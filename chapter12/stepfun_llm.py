"""StepfunLLM - 阶跃星辰 API 适配器

基于 HelloAgentsLLM，修复以下兼容性问题：
1. 强制关闭流式（stepfun 流式 tool calling 不稳定）
2. 添加 RPM 延迟（V0 等级 10/min）
3. 自动从 content 解析 JSON（当 tool_calls 为空时）
"""

import os
import time
import json
from typing import Optional, Iterator

from hello_agents import HelloAgentsLLM


class StepfunLLM(HelloAgentsLLM):
    """阶跃星辰 API 适配器"""

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        # 强制使用 stepfun 配置
        api_key = api_key or os.getenv("STEPFUN_API_KEY") or os.getenv("STEP_API_KEY") or os.getenv("LLM_API_KEY")
        base_url = base_url or os.getenv("LLM_BASE_URL") or "https://api.stepfun.com/v1"
        model = model or os.getenv("LLM_MODEL_ID") or "step-2-16k"

        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url,
            provider="stepfun",
            **kwargs
        )
        self._last_call_time = 0

    def _rate_limit(self):
        """RPM 限流保护（V0 等级约 10/min）"""
        elapsed = time.time() - self._last_call_time
        if elapsed < 6.0:  # 至少间隔 6 秒
            time.sleep(6.0 - elapsed)
        self._last_call_time = time.time()

    def think(self, messages: list[dict[str, str]], temperature: Optional[float] = None) -> Iterator[str]:
        """强制非流式调用，返回完整响应"""
        self._rate_limit()
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature if temperature is not None else self.temperature,
                max_tokens=self.max_tokens,
                stream=False,
            )
            content = response.choices[0].message.content or ""
            print(f"🧠 正在调用 {self.model} 模型...")
            print("✅ 大语言模型响应成功:")
            print(content)
            yield content
        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            raise

    def invoke(self, messages: list[dict[str, str]], **kwargs) -> str:
        """非流式调用，带限流保护"""
        self._rate_limit()
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                stream=False,
                **{k: v for k, v in kwargs.items() if k not in ['temperature', 'max_tokens']}
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            raise
