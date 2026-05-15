# Chapter 15 - 赛博小镇（AI Town）

## 文件

位于 `chapter15/Helloagents-AI-Town/backend/`：

| 文件 | 内容 | 状态 |
|------|------|------|
| `main.py` | FastAPI 主程序 | ✅ import 通过 |
| `config.py` | 配置 | ✅ |
| `models.py` | 数据模型 | ✅ |
| `agents/` | NPC Agent 管理 | ✅ import 通过 |
| `state_manager.py` | 状态管理器 | ✅ import 通过 |

## 依赖安装

```bash
pip install hello-agents
pip install fastapi uvicorn
pip install python-dotenv
```

## 运行

```bash
cd chapter15/Helloagents-AI-Town/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8003
```

## 核心适配

### NPC 状态管理

`main.py` 的 lifespan 初始化会启动 NPC 状态管理器（异步任务），涉及：
- 初始化 NPC 管理器
- 启动状态更新定时器

**当前状态**：import 链路全通，但 lifespan 异步初始化在 nohup 后台模式下可能卡住。前台运行（不加 `&`）可以正常看到启动日志。

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| lifespan 初始化卡住 | 后台启动后 curl 无响应 | 前台运行 `uvicorn main:app`，观察日志 |
| NPC 状态管理器依赖 | 需要异步上下文 | 确保使用支持 async 的 uvicorn 版本 |

## 验证结果

- `python -c "from main import app; print('OK')"`：import 通过 ✅
- 前端启动需进一步验证（涉及 WebSocket / 异步生命周期）
