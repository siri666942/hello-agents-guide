# Chapter 14 - 深度研究助手

## 文件

位于 `chapter14/helloagents-deepresearch/backend/src/`：

| 文件 | 内容 | 状态 |
|------|------|------|
| `main.py` | FastAPI 入口 | ✅ 可启动 |
| `agent.py` | DeepResearchAgent | ✅ import 通过 |
| `config.py` | 配置 | ✅ |
| `models.py` | 数据模型 | ✅ |
| `services/` | 服务层（planner, reporter, search, summarizer） | ✅ import 通过 |

## 依赖安装

```bash
pip install hello-agents
pip install fastapi uvicorn loguru
pip install python-dotenv
```

## 运行

```bash
cd chapter14/helloagents-deepresearch/backend/src
python -m uvicorn main:app --host 0.0.0.0 --port 8002
```

## 核心适配

### ToolAwareSimpleAgent

原 `agent.py` import `ToolAwareSimpleAgent`，但 `hello_agents` 包内无此名称。已修复：

```python
# hello_agents/agents/__init__.py
ToolAwareSimpleAgent = SimpleAgent
```

### NoteTool

原 `agent.py` 还 import `NoteTool`，该工具已存在于 `hello_agents.tools.builtin.note_tool`。

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| `ToolAwareSimpleAgent` 不存在 | `ImportError` | 在 `agents/__init__.py` 设置别名 |

## 验证结果

- 后端启动成功，Swagger UI 可访问：`http://localhost:8002/docs` ✅
