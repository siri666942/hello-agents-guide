# Chapter 4 - LLM 客户端

## 文件

| 文件 | 内容 |
|------|------|
| `llm_client.py` | LLM 客户端封装 |
| `Plan_and_solve.py` | 计划求解 Agent |
| `ReAct.py` | ReAct Agent |
| `Reflection.py` | 反射 Agent |
| `tools.py` | 工具定义 |

## 依赖安装

```bash
pip install python-dotenv openai
```

## 运行

```bash
cd chapter4
python llm_client.py
```

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| 无 `.env` 配置 | API key 未找到 | 在 `/tmp/hello-agents/.env` 写入 `LLM_API_KEY` 和 `LLM_BASE_URL` |
| 使用 `HelloAgentsLLM()` 报错 | 认证失败 | 本指南已统一替换为 `StepfunLLM()`，自动读取 `.env` |

## 说明

本章代码较早期，与后续章节的 `hello_agents` 包结构有差异。重点是理解 LLM 调用方式，代码可直接运行验证基本概念。
