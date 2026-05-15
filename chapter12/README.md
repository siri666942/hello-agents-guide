# Chapter 12 - 评估与数据生成

## 文件

| 文件 | 内容 | 状态 |
|------|------|------|
| `01_basic_agent_example.py` | 基础 Agent 示例 | ✅ 通过 |
| `02_bfcl_quick_start.py` | BFCL 快速开始 | — |
| `03_bfcl_custom_evaluation.py` | BFCL 自定义评估 | — |
| `04_run_bfcl_evaluation.py` | 运行 BFCL 评估 | — |
| `05_gaia_quick_start.py` | GAIA 快速开始 | — |
| `06_gaia_best_practices.py` | GAIA 最佳实践 | — |
| `07_data_generation_complete_flow.py` | 数据生成完整流程 | — |
| `08_data_generation_llm_judge.py` | LLM 裁判 | — |
| `09_data_generation_win_rate.py` | 胜率评估 | — |
| `stepfun_llm.py` | StepfunLLM 适配器 | ✅ |

## 依赖安装

```bash
pip install hello-agents
pip install python-dotenv openai
pip install serpapi google-search-results
pip install gradio
```

## 运行

```bash
cd chapter12
python 01_basic_agent_example.py
```

## 核心适配

### SearchTool

原 `hello_agents.tools` 未导出 `search` 函数，已修复 `tools/__init__.py`：

```python
from .builtin.search import SearchTool, search
```

### StepfunLLM

本章已替换为 `StepfunLLM`，文件已复制到本章目录。

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| `SearchTool` 未导出 | `ImportError` | 已修复 `tools/__init__.py` |
| `serpapi` 未安装 | 搜索工具初始化失败 | `pip install serpapi google-search-results` |
| Tavily API key 未设置 | `Tavily search failed: Unauthorized` | 在 `.env` 中加入 `TAVILY_API_KEY`（可选，有 fallback） |
| SERPAPI key 未设置 | `SERPAPI_API_KEY未设置` | 在 `.env` 中加入 `SERPAPI_API_KEY`（可选，有 fallback） |

## 验证结果

- `01_basic_agent_example.py`：Agent + SearchTool + StepfunLLM 全部正常 ✅
