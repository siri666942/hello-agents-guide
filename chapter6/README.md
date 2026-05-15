# Chapter 6 - 四框架实战

## 文件

仓库在 `Co-creation-projects/YYHDBL-HelloCodeAgentCli/` 下，本章对应 `code/chapter6/`：

| 目录 | 框架 | 状态 |
|------|------|------|
| `AutoGenDemo/` | AutoGen | ✅ 通过 |
| `CAMEL/` | CAMEL | ✅ 通过 |
| `LangGraph/` | LangGraph | ✅ 通过 |
| `AgentScopeDemo/` | AgentScope | ⚠️ stepfun 兼容性问题 |

## 依赖安装

```bash
pip install autogen==0.7.4
pip install camel-ai
pip install langgraph langchain langchain-openai tavily-python
pip install agentscope
```

## 运行

```bash
cd code/chapter6/AutoGenDemo
python autogen_software_team.py

cd code/chapter6/CAMEL
python DigitalBookWriting.py

cd code/chapter6/LangGraph
python main.py
```

## AgentScope 踩坑（重点）

### 问题

stepfun API 与 AgentScope 的 `ReActAgent` 不兼容，因为：
- AgentScope 使用 OpenAI SDK 的 `client.chat.completions.parse()`（结构化输出）
- stepfun 对 `parse()` 的支持有 bug：`tool_calls.function.name` 返回空字符串

### 解决选项

| 方案 | 操作 | 结果 |
|------|------|------|
| A | 跳过 AgentScope | 标记为 stepfun 兼容性问题 |
| B | 改 AgentScope 源码 | 把 `parse` 改为 `create` + 手动 JSON 解析（工作量大） |
| C | 换 API 提供商 | 用 OpenAI / DeepSeek / 智谱等完整兼容的 key |

### 补丁（如需临时绕过）

在 `venv/lib/python3.12/site-packages/agentscope/model/_openai_model.py` 中：

找到 `_parse_openai_stream_response` 和 `_parse_openai_completion_response`，在解析 `tool_call.function.name` 时，若为空则默认设为 `"generate_response"`。

## 说明

- AutoGen / CAMEL / LangGraph 在 stepfun 下均可正常运行
- AgentScope 的问题**不是 stepfun 独有**，是与各类非 OpenAI "OpenAI-compatible" API 的普遍兼容性问题
