# Codex Patent Workbench

Agent-agnostic patent deduplication workbench for an existing patent knowledge base.

这个项目的职责很收敛：先扫描已有专利库，建立“专利号级别”的统一索引，然后为任何 agent 提供稳定的候选专利去重能力。

它不是只给 Codex 使用的。任何 agent 只要能做到下面任一项，都可以复用它：
- 调用命令行
- 写入候选专利 JSON 文件
- 读取 JSON 输出结果

## Features

- Scan an existing patent knowledge base and build a reusable inventory index
- Normalize patent ids like `CN118302107A`, `US20250012345A1`, `WO2026999999A1`
- Deduplicate candidate patents against:
  - existing downloaded files
  - OCR records
  - analysis reports
  - duplicates within the current candidate batch
- Expose a stable CLI for other agents and workflows
- Inspect a single patent record and all of its known file occurrences

## Repository Layout

```text
codex-patent-workbench/
├── examples/
├── src/codex_patent_workbench/
├── tests/
├── README.md
├── SKILL.md
├── LICENSE
└── pyproject.toml
```

## Supported File Shapes

The inventory builder recognizes the same patent across multiple file shapes, including:

- `*.pdf`
- `*_ocr.md`
- `*.pdf_ocr.md`
- `*_YYYYMMDD.md`
- `*_分析_YYYY-MM-DD.md`
- `*_pageN.png`

This matters because a single patent may exist as raw PDF, OCR output, page renders, and analysis notes at the same time.

## Configuration

By default, the project reads from:

- `~/Desktop/专利知识库/专利原文/`
- `~/Desktop/专利知识库/专利分析报告/`
- `~/Desktop/专利知识库/logs/patent_ocr_done.json`

You can override paths with environment variables:

```bash
export PATENT_WORKBENCH_BASE_DIR=/path/to/专利知识库
export PATENT_WORKBENCH_RAW_DIR=/path/to/raw
export PATENT_WORKBENCH_ANALYSIS_DIR=/path/to/analysis
export PATENT_WORKBENCH_LOGS_DIR=/path/to/logs
export PATENT_WORKBENCH_OCR_DONE_FILE=/path/to/patent_ocr_done.json
export PATENT_WORKBENCH_OUTPUT_DIR=/path/to/output
```

## Installation

### Option 1: Run directly

```bash
cd /Users/liutao/.hermes/skills/productivity/codex-patent-workbench
PYTHONPATH=src python3 -m codex_patent_workbench.cli summary
```

### Option 2: Install in a virtual environment

This is the recommended setup for other agents and shared automation.

```bash
cd /Users/liutao/.hermes/skills/productivity/codex-patent-workbench
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

After installation:

```bash
codex-patent-workbench build-index
codex-patent-workbench summary
codex-patent-workbench filter-candidates --input examples/candidates.sample.json
codex-patent-workbench inspect-patent CN118302107A
```

## CLI

### Build or rebuild the inventory index

```bash
codex-patent-workbench build-index
```

### Show inventory summary

```bash
codex-patent-workbench summary
```

### Filter candidate patents

```bash
codex-patent-workbench filter-candidates --input examples/candidates.sample.json
```

### Inspect a known patent

```bash
codex-patent-workbench inspect-patent CN118302107A
```

## Agent Integration Contract

Recommended integration flow:

1. An upstream agent searches for candidate patents
2. It writes them as a JSON list
3. It calls `codex-patent-workbench filter-candidates`
4. It only processes `unique_candidates`
5. It logs `duplicate_candidates` and `invalid_candidates`

Input example:

See [examples/candidates.sample.json](./examples/candidates.sample.json).

Output example:

See [examples/filter-output.sample.json](./examples/filter-output.sample.json).

The filter output contains:

- `unique_candidates`
- `duplicate_candidates`
- `invalid_candidates`
- `stats`
- `output_file`

## Why This Exists

Many patent pipelines accidentally reprocess the same patent because the same underlying record can appear in different places:

- existing PDF downloads
- OCR-generated markdown
- rendered page images
- separate analysis reports
- repeated discovery from multiple search tools

This project makes deduplication the default behavior, not a cleanup step after the fact.

## Development

Run local tests:

```bash
cd /Users/liutao/.hermes/skills/productivity/codex-patent-workbench
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
```

## Design Principles

- Do not modify Hermes internals
- Use patent id, not filename, as the primary key
- Normalize first, deduplicate second, process third
- Keep outputs auditable and reusable
- Stay simple enough for any agent to call

## License

MIT. See [LICENSE](./LICENSE).
