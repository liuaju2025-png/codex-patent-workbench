---
name: codex-patent-workbench
title: Codex 专利情报工作台
description: 使用独立工作台为专利知识库做去重索引、候选专利过滤、标准化落盘与后续分析，不修改 Hermes 现有实现。
tags: [专利, 去重, 知识库, codex, 行业分析]
version: 0.1.0
created: 2026-05-10
---

# Codex 专利情报工作台

这是一个独立于 Hermes 的专利工作台 skill。

目标：
- 不修改 Hermes 现有脚本和目录逻辑
- 直接复用现有专利知识库
- 先扫描现有已下载专利，建立统一专利号索引
- 所有新候选专利先过去重，再进入后续下载、摘要、分析流程
- 通过 CLI + JSON 接口让其他 agent 也能直接调用

## 当前能力

### 1. 扫描现有知识库并建立去重索引

扫描目录：
- `~/Desktop/专利知识库/专利原文/`
- `~/Desktop/专利知识库/专利分析报告/`
- `~/Desktop/专利知识库/logs/patent_ocr_done.json`

识别并统一专利号级别去重，不受以下文件形态影响：
- `*.pdf`
- `*_ocr.md`
- `*.pdf_ocr.md`
- `*_YYYYMMDD.md`
- `*_分析_YYYY-MM-DD.md`
- `*_pageN.png`

### 2. 候选专利过滤

输入一个 JSON 文件，包含候选专利记录列表，自动：
- 规范化专利号
- 与现有知识库索引比对
- 标记重复 / 新增
- 输出过滤后的新增列表

### 3. 独立落盘

索引与输出保存到：
- `~/Desktop/专利知识库/codex_workbench/`

不会覆盖 Hermes 现有文件。

### 4. 可供其他 agent 复用

这个 skill 不依赖 Codex 专属上下文。

其他 agent 只要满足以下任一条件即可使用：
- 能调用 shell 命令
- 能写 JSON 文件
- 能读取 JSON 结果

建议把它当成一个“专利候选去重网关”：
- 上游 agent 负责搜索候选专利
- 本工作台负责索引、归一化、去重
- 下游 agent 只处理 `unique_candidates`

## CLI

### 重建索引

```bash
codex-patent-workbench build-index
```

### 查看索引摘要

```bash
codex-patent-workbench summary
```

### 过滤候选专利

```bash
codex-patent-workbench filter-candidates --input /path/to/candidates.json
```

输入格式示例：

```json
[
  {
    "patent_id": "CN118302107A",
    "title": "一种共封装光学装置",
    "sector": "CPO共封装光学",
    "source": "manual"
  },
  {
    "patent_id": "US20250012345A1",
    "title": "Cooling system for AI servers",
    "sector": "AI服务器液冷",
    "source": "manual"
  }
]
```

## 实现原则

- 去重是默认行为，不是后处理步骤
- 以“专利号”作为主键，而不是文件名
- 多来源数据先归一化，再决定是否写入知识库
- 索引构建结果必须可复用、可审计、可导出

## 下一步建议

后续可以在这个工作台上继续加：
- Tavily / QCC / Web 搜索适配器
- 自动落盘 Markdown 模板
- 周报 / 月报生成
- OCR / 摘要 / 分析状态机
