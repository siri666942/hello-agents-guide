# 《Hello Agents》实操补充指南

> 本文档补充原教程中缺失的实践细节——**怎么装、怎么跑、踩了什么坑**。
> 知识类内容参见原教程，本文档只关心"让代码跑起来"。

---

## 环境准备（全章节通用）

### 1. 创建虚拟环境

```bash
cd /tmp/hello-agents
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
```

### 2. 安装核心包

```bash
pip install hello-agents  # 或从源码安装
pip install python-dotenv openai
```

### 3. 配置 LLM API

在 `/tmp/hello-agents/.env` 中写入你的 API 配置：

```env
# 示例：使用 stepfun（阶跃星辰）
LLM_API_KEY=你的_api_key
LLM_BASE_URL=https://api.stepfun.com/v1
LLM_MODEL_ID=step-3.5-flash

# 你也可以换其他 OpenAI-compatible 提供商：
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL_ID=gpt-4o-mini
# LLM_BASE_URL=https://api.deepseek.com/v1
# LLM_MODEL_ID=deepseek-chat
```

**注意：**
- 本教程示例使用 stepfun，但**代码不绑定任何特定提供商**
- 只要 API 兼容 OpenAI 格式，换 `LLM_BASE_URL` 和 `LLM_MODEL_ID` 即可
- stepfun V0 等级 RPM 限制约 10/min，调用需间隔 ≥ 6 秒
- stepfun 流式 tool calling 不稳定，**必须关闭流式模式**

### 4. 核心适配文件

本指南提供 `StepfunLLM` 适配器（示例），特性：
- 强制非流式调用
- 内置 RPM 限流保护
- 自动读取 `.env` 配置

适配器位置：`code/chapter7/stepfun_llm.py`（后续章节已复制到各自目录）

**使用其他提供商时**：直接调用 `HelloAgentsLLM()` 即可，或参考 `StepfunLLM` 写自己的适配器。

---

## 全局踩坑记录

| 坑 | 现象 | 解决方案 |
|---|---|---|
| stepfun 不支持 tool calls | `400 - tool_calls.function.name is required` | 换 step-2-16k 模型，或在 `agentscope/_openai_model.py` 打补丁（见 Chapter 6） |
| stepfun 流式解析失败 | `tool_calls.function.name is required` | 强制 `stream=False` |
| 包内绝对导入错误 | `ModuleNotFoundError: No module named 'core'` | 从源码 `pip install -e .` 安装 hello-agents 包 |
| `hello_agents` 缺 `CalculatorTool` | `ImportError: cannot import name 'CalculatorTool'` | 用本地 `calculator_tool.py` 或安装到 site-packages |
| `hello_agents` 缺 `MemoryTool`/`RAGTool` | `ModuleNotFoundError: No module named 'memory'` | 使用简化占位实现（见 Chapter 8） |
| `hello_agents` 缺 `SearchTool` 导出 | `ImportError: cannot import name 'SearchTool'` | 修改 `tools/__init__.py` 添加 `search` 导出 |
| `ToolAwareSimpleAgent` 不存在 | `ImportError: cannot import name 'ToolAwareSimpleAgent'` | 在 `agents/__init__.py` 设置别名 `ToolAwareSimpleAgent = SimpleAgent` |
| 检查脚本误报同目录导入 | 大量 `Missing` 误报 | 忽略，运行时 Python 能找到同目录文件 |

---

## 各章节导航

| 章节 | 内容 | 关键依赖 | README |
|------|------|----------|--------|
| Ch1 | 第一个 Agent | 无 | [chapter1/README.md](chapter1/README.md) |
| Ch2 | ELIZA | 无 | [chapter2/README.md](chapter2/README.md) |
| Ch3 | 基础原理 | torch, transformers | [chapter3/README.md](chapter3/README.md) |
| Ch4 | LLM 客户端 | hello-agents, dotenv | [chapter4/README.md](chapter4/README.md) |
| Ch5 | （空） | — | — |
| Ch6 | 四框架 | agentscope, autogen, camel, langgraph | [chapter6/README.md](chapter6/README.md) |
| Ch7 | Agent 架构 | hello-agents | [chapter7/README.md](chapter7/README.md) |
| Ch8 | 记忆与检索 | hello-agents | [chapter8/README.md](chapter8/README.md) |
| Ch9 | 上下文工程 | hello-agents | [chapter9/README.md](chapter9/README.md) |
| Ch10 | 通信协议 | fastmcp, a2a-sdk(可选) | [chapter10/README.md](chapter10/README.md) |
| Ch11 | Agentic RL | datasets, transformers | [chapter11/README.md](chapter11/README.md) |
| Ch12 | 评估与数据 | serpapi, gradio | [chapter12/README.md](chapter12/README.md) |
| Ch13 | 旅行助手 | fastapi, uvicorn | [chapter13/README.md](chapter13/README.md) |
| Ch14 | 深度研究 | fastapi, uvicorn, loguru | [chapter14/README.md](chapter14/README.md) |
| Ch15 | AI Town | fastapi, uvicorn | [chapter15/README.md](chapter15/README.md) |
| Ch16 | 毕业设计 | 文档 | [chapter16/README.md](chapter16/README.md) |
