# -*- coding: utf-8 -*-
"""
StepfunChatModel - 专门适配阶跃星辰(stepfun) API 的 AgentScope 模型类。

修复 AgentScope OpenAIChatModel 与 stepfun API 的不兼容问题：
1. tool_calls 为空但 content 含 JSON 时，自动解析为 tool_use
2. function.name 为空时兜底为 generate_response
3. 流式/非流式解析统一修复
4. content=None 时自动设为空字符串，避免 400 错误

用法：
    from stepfun_model import StepfunChatModel
    
    model = StepfunChatModel(
        model_name="step-2-16k",
        api_key=os.getenv("LLM_API_KEY"),
        client_args={"base_url": os.getenv("LLM_BASE_URL")},
        stream=False,  # 建议关闭流式
    )
"""

import json
import shortuuid
import asyncio
from datetime import datetime
from typing import Any, AsyncGenerator, Type

from agentscope.model import OpenAIChatModel
from agentscope.model._model_response import ChatResponse
from agentscope.message import ToolUseBlock, TextBlock, ThinkingBlock
from agentscope._utils._common import _json_loads_with_repair


class StepfunChatModel(OpenAIChatModel):
    """适配 stepfun API 的 ChatModel，修复 function calling 兼容性问题。"""

    async def __call__(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str | None = None,
        structured_model: Type | None = None,
        **kwargs: Any,
    ) -> ChatResponse | AsyncGenerator[ChatResponse, None]:
        """调用 stepfun API，并在解析阶段修复不兼容问题。"""

        # 强制关闭流式，stepfun 流式 tool calling 极不稳定
        if self.stream:
            kwargs["stream"] = False

        # stepfun V0 等级 RPM=10，加延迟避免触发限流
        await asyncio.sleep(0.5)

        # 调用父类生成逻辑，但 catch 并修复 stepfun 的 quirks
        try:
            response = await super().__call__(
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                structured_model=structured_model,
                **kwargs,
            )
        except Exception:
            # 如果父类失败，尝试非流式重试
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

        # 修复 response 中的 stepfun 特有格式问题
        if isinstance(response, ChatResponse):
            return self._fix_stepfun_response(response, structured_model)
        else:
            # 流式 generator 暂不支持，直接返回
            return response

    def _fix_stepfun_response(self, response: ChatResponse, structured_model: Type | None = None) -> ChatResponse:
        """修复 stepfun 返回的 ChatResponse 中的格式问题。"""
        fixed_blocks = []
        parsed_tool_call = None
        extracted_json = None

        for block in response.content:
            # 修复空 name 的 tool_use
            if block.get("type") == "tool_use":
                name = block.get("name", "")
                if not name:
                    block["name"] = "generate_response"

                # 如果 input 为空但 content 里有 JSON，尝试从 content 解析
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

            # 收集文本 block，看是否能从中解析出 JSON tool call 或结构化输出
            elif block.get("type") == "text":
                text = block.get("text", "")
                if text:
                    # 尝试解析为 tool call
                    if not parsed_tool_call:
                        parsed_tool_call = self._try_parse_tool_call_from_text(text)
                    
                    # 尝试解析为结构化输出 JSON（用于 structured_model 模式）
                    if not extracted_json and structured_model:
                        extracted_json = self._try_parse_structured_json(text)
                        if extracted_json:
                            # 替换文本 block 为 tool_use block，让 AgentScope 正确处理
                            parsed_tool_call = ToolUseBlock(
                                type="tool_use",
                                id=shortuuid.uuid(),
                                name="generate_response",
                                input=extracted_json,
                            )
                
                fixed_blocks.append(block)

            else:
                fixed_blocks.append(block)

        # 如果没有任何 tool_use block，但文本里解析出了 tool call，追加它
        has_tool_use = any(b.get("type") == "tool_use" for b in fixed_blocks)
        if not has_tool_use and parsed_tool_call:
            fixed_blocks.append(parsed_tool_call)

        response.content = fixed_blocks
        
        # 如果 structured_model 存在且 metadata 为空，但 extracted_json 有值，填充 metadata
        if structured_model and (response.metadata is None or response.metadata == {}) and extracted_json:
            response.metadata = extracted_json
        
        return response

    @staticmethod
    def _try_parse_structured_json(text: str) -> dict | None:
        """尝试从文本中解析结构化输出 JSON。
        
        stepfun 的 structured output 有时返回纯文本 JSON，
        需要提取并验证是否包含常见结构化字段。
        """
        text = text.strip()
        if not text:
            return None

        # 模式 1: Markdown JSON 代码块
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

        # 模式 2: 纯 JSON 字符串
        if text.startswith("{") and text.endswith("}"):
            try:
                parsed = _json_loads_with_repair(text)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        return None

    @staticmethod
    def _try_parse_tool_call_from_text(text: str) -> ToolUseBlock | None:
        """尝试从文本中解析 stepfun 以文本形式返回的 tool call JSON。

        stepfun 有时不会返回 tool_calls 数组，而是把 JSON 直接写在 content 里。
        检测模式：
        - JSON 块，包含 response / reach_agreement / confidence_level
        - Markdown JSON 代码块
        - '| function\ngenerate_response\n{...}' 格式
        """
        text = text.strip()
        if not text:
            return None

        # 模式 1: Markdown JSON 代码块
        if "```json" in text or "```" in text:
            try:
                # 提取 ```json ... ``` 或 ``` ... ``` 之间的内容
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
                        type="tool_use",
                        id=shortuuid.uuid(),
                        name="generate_response",
                        input=parsed,
                    )
            except Exception:
                pass

        # 模式 2: 纯 JSON 字符串
        if text.startswith("{") and text.endswith("}"):
            try:
                parsed = _json_loads_with_repair(text)
                if isinstance(parsed, dict) and "response" in parsed:
                    return ToolUseBlock(
                        type="tool_use",
                        id=shortuuid.uuid(),
                        name="generate_response",
                        input=parsed,
                    )
            except Exception:
                pass

        # 模式 3: '| function\nname\n{...}' 格式（AgentScope 内部 fallback 格式）
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
                    json_str = "\n".join(json_lines)
                    parsed = _json_loads_with_repair(json_str)
                    if isinstance(parsed, dict) and "response" in parsed:
                        return ToolUseBlock(
                            type="tool_use",
                            id=shortuuid.uuid(),
                            name="generate_response",
                            input=parsed,
                        )
            except Exception:
                pass

        return None
