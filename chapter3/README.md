# Chapter 3 - 基础原理

## 文件

| 文件 | 内容 | 是否需要 GPU |
|------|------|-------------|
| `BPE.py` | BPE 分词算法 | 否 |
| `N_gram.py` | N-gram 语言模型 | 否 |
| `Word_Embedding.py` | 词向量与类比 | 否 |
| `Transformer.py` | Transformer 编码器 | 否（CPU可跑） |
| `Qwen.py` | 加载 Qwen 模型做推理 | 否（CPU可跑，慢） |

## 依赖安装

```bash
pip install torch torchvision transformers
```

## 运行

```bash
cd chapter3

# 基础算法（无模型下载，秒级运行）
python BPE.py
python N_gram.py
python Word_Embedding.py
python Transformer.py

# 模型推理（需下载 Qwen1.5-0.5B-Chat，约 1GB，首次慢）
python Qwen.py
```

## 坑

| 坑 | 现象 | 解决方案 |
|---|---|---|
| HuggingFace 下载慢/断 | `Connection aborted` | 脚本已设 `HF_ENDPOINT=https://hf-mirror.com`，无需处理 |
| 模型下载超时 | 进程被 kill | 网络问题，重试或换网络环境 |
| CPU 推理极慢 | 等了半天没输出 | 正常现象，0.5B 模型 CPU 推理需几分钟，耐心等 |
| CUDA 不可用 | `CUDA available: False` | 没关系，CPU 也能跑 |

## 注意

- `Qwen.py` 下载模型权重是**最耗时的一步**，首次运行需 5-15 分钟
- 如果不需要真实模型推理，前 4 个文件已足够理解原理
