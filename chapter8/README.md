# Chapter 8 - 记忆与检索

## 文件

| 文件 | 内容 | 状态 |
|------|------|------|
| `08_Agent_Tool_Integration.py` | 记忆+RAG+Agent集成演示 | ✅ 通过 |
| `01_MemoryTool_Basic_Operations.py` | MemoryTool 基础操作 | — |
| `02_MemoryTool_Architecture.py` | MemoryTool 架构 | — |
| `03_WorkingMemory_Implementation.py` | 工作记忆实现 | — |
| `04_RAGTool_MarkItDown_Pipeline.py` | RAG Pipeline | — |
| `05_RAGTool_Advanced_Search.py` | RAG 高级搜索 | — |
| `06_Memory_Consolidation_Demo.py` | 记忆巩固演示 | — |
| `07_RAGTool_Intelligent_QA.py` | RAG 智能问答 | — |
| `09_Memory_Types_Deep_Dive.py` | 记忆类型深度解析 | — |
| `10_RAG_Pipeline_Complete.py` | 完整 RAG Pipeline | — |

## 依赖安装

```bash
pip install hello-agents
pip install python-dotenv openai
```

## 运行

```bash
cd chapter8
python 08_Agent_Tool_Integration.py
```

## 核心适配

### MemoryTool / RAGTool

原 `hello_agents` 包内的 `MemoryTool` / `RAGTool` 依赖外部服务（qdrant、neo4j），安装复杂。本指南采用**简化占位实现**：

- `MemoryTool`：基于字典的内存存储，不依赖外部数据库
- `RAGTool`：基于列表的文档检索，不依赖向量数据库

这些占位实现已安装到 site-packages 下的 `hello_agents/tools/builtin/`，import 路径完全兼容。

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| qdrant/neo4j 依赖地狱 | `pip install` 卡住 | 使用简化占位实现，跳过外部依赖 |
| `MemoryTool` 未导出 | `ImportError` | 已修复 `tools/__init__.py` 导出 |
| `RAGTool` 文件缺失 | 包内无此文件 | 已创建占位实现 |

## 验证结果

- `08_Agent_Tool_Integration.py`：Memory + RAG + Agent 全部正常 ✅
