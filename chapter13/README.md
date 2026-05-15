# Chapter 13 - 智能旅行助手

## 文件

位于 `chapter13/helloagents-trip-planner/backend/`：

| 目录 | 内容 | 状态 |
|------|------|------|
| `app/api/main.py` | FastAPI 主应用 | ✅ 可启动 |
| `app/api/routes/` | API 路由（trip, poi, map） | ✅ |
| `app/config.py` | 配置管理 | ✅ |
| `app/agents/` | Agent 实现 | ✅ import 通过 |
| `app/services/` | 业务服务 | ✅ import 通过 |

## 依赖安装

```bash
pip install hello-agents
pip install fastapi uvicorn pydantic-settings
pip install python-dotenv
```

## 运行

```bash
cd chapter13/helloagents-trip-planner/backend

# 启动前确保 .env 已配置
python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8001
```

## 配置

在 `backend/.env` 中写入：

```env
LLM_API_KEY=你的_stepfun_key
LLM_BASE_URL=https://api.stepfun.com/v1
LLM_MODEL_ID=step-1-8k
AMAP_API_KEY=placeholder_for_demo
UNPLASH_API_KEY=placeholder
```

**注意**：`AMAP_API_KEY` 和 `UNPLASH_API_KEY` 是启动必需的（config 验证会检查），但运行时可以填 placeholder。如需真实地图/图片功能，需要去对应平台申请免费 key。

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| `AMAP_API_KEY未配置` | 启动失败 `ValueError` | 在 `.env` 中加入 `AMAP_API_KEY`（placeholder 也行） |
| 相对导入错误 | `attempted relative import beyond top-level` | 用 `python -m uvicorn app.api.main:app` 启动（加 `-m`） |
| 高德 API key 缺失 | 地图功能不可用 | 申请高德开放平台 key（免费） |

## 验证结果

- 后端启动成功，Swagger UI 可访问：`http://localhost:8001/docs` ✅
