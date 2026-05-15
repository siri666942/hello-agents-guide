# Chapter 7 - Agent 架构

## 文件

| 文件 | 内容 | 状态 |
|------|------|------|
| `test_simple_agent.py` | SimpleAgent 全量测试 | ✅ 通过 |
| `test_plan_solve_agent.py` | PlanAndSolveAgent 测试 | ✅ 通过 |
| `my_simple_agent.py` | SimpleAgent 包装 | ✅ |
| `my_react_agent.py` | ReActAgent 包装 | ✅ |
| `my_reflection_agent.py` | ReflectionAgent 包装 | ✅ |
| `my_plan_solve_agent.py` | PlanAndSolveAgent 包装 | ✅ |
| `my_llm.py` | 本地 LLM 包装 | ✅ |
| `calculator_tool.py` | 本地计算器工具 | ✅ |
| `stepfun_llm.py` | StepfunLLM 适配器 | ✅ |

## 依赖安装

```bash
# 核心包
pip install hello-agents  # 或从源码 pip install -e .

# 外部依赖
pip install python-dotenv openai
```

## 运行

```bash
cd chapter7

# 测试 SimpleAgent（基础对话/工具调用/流式/动态工具）
python test_simple_agent.py

# 测试 PlanAndSolveAgent（计划分解 + 逐步执行）
python test_plan_solve_agent.py
```

## 核心适配

### StepfunLLM

本章及后续章节使用 `StepfunLLM` 作为示例适配器（替换原教程的 `HelloAgentsLLM()`）：

```python
from stepfun_llm import StepfunLLM
llm = StepfunLLM()
```

特性：
- 强制非流式调用（`stream=False`）
- 6 秒 RPM 限流保护
- 自动读取 `.env` 中的 `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL_ID`

**使用其他提供商时**：直接调用 `HelloAgentsLLM()`，或参考 `StepfunLLM` 写自己的适配器。

### CalculatorTool

原 `hello_agents` 包内无 `CalculatorTool` 实现，本章提供本地版本：

```python
from calculator_tool import CalculatorTool
```

同时已补充到 `hello_agents.tools` 导出（site-packages 下）。

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| `hello_agents` 未安装 | `ModuleNotFoundError` | `pip install -e .` 从源码安装 |
| 绝对导入错误 | `No module named 'core'` | 安装包后修复了导入路径 |
| `CalculatorTool` 不存在 | `ImportError` | 用本地 `calculator_tool.py` 或更新包导出 |
| 流式 tool calling 失败 | stepfun 返回空 name | `StepfunLLM` 已强制 `stream=False` |
| RPM 超限 | 429 错误 | `StepfunLLM` 内置 6 秒限流 |

## 验证结果

- `test_simple_agent.py`：4 项测试全部通过 ✅
- `test_plan_solve_agent.py`：计划执行正确（70 个苹果）✅
