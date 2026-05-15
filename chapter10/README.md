# Chapter 10 - 通信协议（MCP / A2A / ANP）

## 文件

| 文件 | 内容 | 状态 |
|------|------|------|
| `01_TestConnect.py` | 协议连接测试 | ✅ 通过 |
| `07_SimpleA2AAgent.py` | A2A 技能系统 | ✅ 通过 |
| `02_Connect2MCP.py` | MCP 连接 | — |
| `03_GitHubMCP.py` | GitHub MCP | — |
| `04_MCPTransport.py` | MCP 传输层 | — |
| `05_UseMCPToolInAgent.py` | Agent 中使用 MCP | — |
| `06_MultiAgentDocumentAssist.py` | 多 Agent 文档协助 | — |
| `08_CustomA2AAgent.py` | 自定义 A2A Agent | — |
| `09_A2A_Client.py` | A2A 客户端 | — |
| `09_A2A_Network.py` | A2A 网络 | — |

## 依赖安装

```bash
pip install hello-agents
pip install python-dotenv openai

# MCP 支持（可选，占位已实现）
pip install fastmcp

# A2A SDK（可选，占位已实现）
# pip install a2a-sdk  # 若安装真实库，占位自动切换
```

## 运行

```bash
cd chapter10

# 协议连接测试（MCP + ANP + A2A）
python 01_TestConnect.py

# A2A 计算器 Agent
python 07_SimpleA2AAgent.py
```

## 核心适配

### 协议工具占位策略

原教程依赖外部库实现 MCP / A2A / ANP，本指南采用**占位实现**：

- `MCPClient`：支持 `__aenter__`/`__aexit__` 异步上下文，基础方法 stub
- `A2AClient` / `A2AServer`：支持 `send_task`、`start`、`skill` 装饰器
- `ANPDiscovery` / `ANPNetwork`：基础服务发现和网络通信 stub

这些占位实现位于：
- `hello_agents/protocols/mcp/client.py`
- `hello_agents/protocols/a2a/implementation.py`
- `hello_agents/protocols/anp/implementation.py`

**优点**：代码可 import、可运行、能看到协议框架结构  
**代价**：非真实网络通信，学习协议结构足够

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| `a2a-sdk` 未安装 | `❌ A2A SDK 未安装` | 占位实现已设为 `A2A_AVAILABLE = True`，无需安装 |
| `MCPTool` 未导出 | `ImportError` | 已修复 `tools/__init__.py` 导出 |
| 异步上下文报错 | `await` 相关 | 占位实现已补全 `__aenter__`/`__aexit__` |

## 验证结果

- `01_TestConnect.py`：MCP + ANP + A2A 全部连接正常 ✅
- `07_SimpleA2AAgent.py`：A2A 技能系统（add/multiply/info）全部正常 ✅
