# Chapter 9 - 上下文工程

## 文件

| 文件 | 内容 | 状态 |
|------|------|------|
| `01_context_builder_basic.py` | 上下文构建基础 | ✅ 通过 |
| `02_context_builder_with_agent.py` | 结合 Agent 使用 | — |
| `03_note_tool_operations.py` | NoteTool 操作 | — |
| `04_note_tool_integration.py` | NoteTool 集成 | — |
| `05_terminal_tool_examples.py` | 终端工具示例 | — |
| `06_three_day_workflow.py` | 三天工作流 | — |
| `calculator_tool.py` | 计算器工具 | ✅ |
| `stepfun_llm.py` | StepfunLLM 适配器 | ✅ |

## 依赖安装

```bash
pip install hello-agents
pip install python-dotenv openai
```

## 运行

```bash
cd chapter9
python 01_context_builder_basic.py
```

## 核心适配

本章使用 `StepfunLLM` 替代 `HelloAgentsLLM()`，文件已复制到本章目录。

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| 缺 `stepfun_llm.py` | `ModuleNotFoundError` | 从 chapter7 复制到本章目录 |

## 验证结果

- `01_context_builder_basic.py`：上下文构建 + LLM 响应正常 ✅
