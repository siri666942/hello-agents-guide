# -*- coding: utf-8 -*-
"""
AdaptiveOpenAIModel - 通用 OpenAI-compatible API 适配器

修复各种 OpenAI-compatible API 的 tool calling 兼容性问题：
1. function.name 为空 → 兜底为 generate_response
2. tool_calls 为空但 content 含 JSON → 自动解析
3. 嵌套 JSON / Markdown JSON → 多模式解析
4. content=None → 设为空字符串
5. 流式/非流式统一修复

用法：
    from adaptive_openai_model import AdaptiveOpenAIModel

    model = AdaptiveOpenAIModel(
        model_name="step-2-16k",
        api_key=os.getenv("LLM_API_KEY"),
        client_args={"base_url": os.getenv("LLM_BASE_URL")},
        stream=False,
    )
"""

import asyncio
import shortuuid
from typing import Any, AsyncGenerator, Type

from agentscope.model import OpenAIChatModel
from agentscope.model._model_response import ChatResponse
from agentscope.message import ToolUseBlock, TextBlock
from agentscope._utils._common import _json_loads_with_repair


class AdaptiveOpenAIModel(OpenAIChatModel):
    """适配各种不完美的 OpenAI-compatible API 的 ChatModel。"""

    async def __call__(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str | None = None,
        structured_model: Type | None = None,
        **kwargs: Any,
    ) -> ChatResponse | AsyncGenerator[ChatResponse, None]:
        """调用 API，并在解析阶段修复兼容性问题。"""

        # 强制关闭流式（大部分国产 API 流式 tool calling 不稳定）
        if self.stream:
            kwargs["stream"] = False

        # 加延迟避免 RPM 限制（V0 等级 10/min）
        await asyncio.sleep(0.5)

        # 调用父类
        try:
            response = await super().__call__(
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                structured_model=structured_model,
                **kwargs,
            )
        except Exception:
            old_stream = self.stream
            self.stream = False
            try:
                response = await super().__call__(
                    messages=messages,
                    tools=tools,
                    tool_choice=tool_choice,
                    structured_model=structured_model,
                    **kwargs,
                )
            finally:
                self.stream = old_stream

        # 修复 response
        if isinstance(response, ChatResponse):
            return self._fix_response(response, structured_model)
        return response

    def _fix_response(
        self, response: ChatResponse, structured_model: Type | None = None
    ) -> ChatResponse:
        """修复各种格式问题。"""
        fixed_blocks = []
        parsed_tool_call = None
        extracted_json = None

        for block in response.content:
            if block.get("type") == "tool_use":
                name = block.get("name", "")
                if not name:
                    block["name"] = "generate_response"

                input_data = block.get("input", {})
                if not input_data or input_data == {}:
                    content = block.get("content", "")
                    if content and isinstance(content, str):
                        try:
                            parsed = _json_loads_with_repair(content)
                            if isinstance(parsed, dict) and "response" in parsed:
                                block["input"] = parsed
                                block["content"] = ""
                        except Exception:
                            pass
                fixed_blocks.append(block)

            elif block.get("type") == "text":
                text = block.get("text", "")
                if text:
                    if not parsed_tool_call:
                        parsed_tool_call = self._try_parse_tool_call(text)
                    if not extracted_json and structured_model:
                        extracted_json = self._try_parse_structured(text)
                        if extracted_json:
                            parsed_tool_call = ToolUseBlock(
                                type="tool_use",
                                id=shortuuid.uuid(),
                                name="generate_response",
                                input=extracted_json,
                            )
                fixed_blocks.append(block)
            else:
                fixed_blocks.append(block)

        has_tool_use = any(b.get("type") == "tool_use" for b in fixed_blocks)
        if not has_tool_use and parsed_tool_call:
            fixed_blocks.append(parsed_tool_call)

        response.content = fixed_blocks
        if structured_model and (response.metadata is None or response.metadata == {}) and extracted_json:
            response.metadata = extracted_json
        return response

    @staticmethod
    def _try_parse_tool_call(text: str) -> ToolUseBlock | None:
        """从文本中解析 tool call JSON。"""
        text = text.strip()
        if not text:
            return None

        # Markdown JSON 代码块
        if "```" in text:
            try:
                start = text.find("```")
                end = text.find("```", start + 3)
                if end == -1:
                    end = len(text)
                code = text[start + 3:end].strip()
                if code.startswith("json"):
                    code = code[4:].strip()
                parsed = _json_loads_with_repair(code)
                if isinstance(parsed, dict) and "response" in parsed:
                    return ToolUseBlock(
                        type="tool_use", id=shortuuid.uuid(),
                        name="generate_response", input=parsed,
                    )
            except Exception:
                pass

        # 纯 JSON
        if text.startswith("{") and text.endswith("}"):
            try:
                parsed = _json_loads_with_repair(text)
                if isinstance(parsed, dict) and "response" in parsed:
                    return ToolUseBlock(
                        type="tool_use", id=shortuuid.uuid(),
                        name="generate_response", input=parsed,
                    )
            except Exception:
                pass

        # '| function\nname\n{...}' 格式
        if "| function" in text or "function" in text[:50]:
            try:
                lines = text.split("\n")
                json_lines = []
                in_json = False
                for line in lines:
                    if line.strip().startswith("{"):
                        in_json = True
                    if in_json:
                        json_lines.append(line)
                if json_lines:
                    parsed = _json_loads_with_repair("\n".join(json_lines))
                    if isinstance(parsed, dict) and "response" in parsed:
                        return ToolUseBlock(
                            type="tool_use", id=shortuuid.uuid(),
                            name="generate_response", input=parsed,
                        )
            except Exception:
                pass

        return None

    @staticmethod
    def _try_parse_structured(text: str) -> dict | None:
        """从文本中解析结构化输出 JSON。"""
        text = text.strip()
        if not text:
            return None

        if "```" in text:
            try:
                start = text.find("```")
                end = text.find("```", start + 3)
                if end == -1:
                    end = len(text)
                code = text[start + 3:end].strip()
                if code.startswith("json"):
                    code = code[4:].strip()
                parsed = _json_loads_with_repair(code)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        if text.startswith("{") and text.endswith("}"):
            try:
                parsed = _json_loads_with_repair(text)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        return None
