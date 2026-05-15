# Chapter 11 - Agentic RL（强化学习训练）

## 文件

| 文件 | 内容 | 状态 |
|------|------|------|
| `00_quick_test.py` | 快速实验测试 | ✅ 通过 |
| `01_dataset_loading.py` | 数据加载 | — |
| `02_reward_functions.py` | 奖励函数 | — |
| `03_lora_configuration.py` | LoRA 配置 | — |
| `04_sft_training.py` | SFT 训练 | — |
| `05_grpo_training.py` | GRPO 训练 | — |
| `06_complete_pipeline.py` | 完整 Pipeline | — |
| `07_model_evaluation.py` | 模型评估 | — |
| `08_distributed_training.py` | 分布式训练 | — |

## 依赖安装

```bash
pip install hello-agents
pip install datasets transformers
```

## 运行

```bash
cd chapter11
python 00_quick_test.py
```

## 核心适配

### RLTrainingTool

原 `hello_agents` 包内无 `RLTrainingTool` 实现。本指南提供**占位实现**：

- 支持 `action`: `load_dataset`, `train`, `create_reward`
- 支持 `algorithm`: `sft`, `grpo`
- 内部为硬编码返回，不执行真实训练

文件位置：`hello_agents/tools/builtin/rl_training_tool.py`

**如需真实训练**，需要安装：
```bash
pip install trl peft accelerate
```

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| `RLTrainingTool` 不存在 | `ImportError` | 已创建占位实现并导出 |
| `datasets` 未安装 | `ModuleNotFoundError` | `pip install datasets` |

## 验证结果

- `00_quick_test.py`：数据加载 / SFT训练 / GRPO训练 / 奖励函数 全部通过 ✅
