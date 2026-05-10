# Codex Patent Workbench

独立专利工作台原型。

它不是只给 Codex 使用的。任何 agent 只要能做到下面任一项，都可以直接复用它：
- 调用命令行
- 写入候选专利 JSON 文件
- 读取 JSON 输出结果

## 安装

```bash
cd /Users/liutao/.hermes/skills/productivity/codex-patent-workbench
python3 -m pip install -e .
```

安装后可直接使用命令：

```bash
codex-patent-workbench build-index
codex-patent-workbench summary
codex-patent-workbench filter-candidates --input /tmp/candidates.json
```

不安装也可以直接运行：

```bash
PYTHONPATH=src python3 -m codex_patent_workbench.cli build-index
PYTHONPATH=src python3 -m codex_patent_workbench.cli summary
PYTHONPATH=src python3 -m codex_patent_workbench.cli filter-candidates --input /tmp/candidates.json
```

## Agent 集成约定

推荐把它当成一个稳定的外部去重服务来调用：

1. agent 先生成候选专利列表 JSON
2. 调用 `codex-patent-workbench filter-candidates`
3. 只对 `unique_candidates` 做后续下载、摘要、分析、入库
4. 把 `duplicate_candidates` 记录到自己的日志或任务结果里

输入示例：

```json
[
  {
    "patent_id": "CN118302107A",
    "title": "一种共封装光学装置",
    "sector": "CPO共封装光学",
    "source": "agent-a"
  },
  {
    "patent_id": "US20250012345A1",
    "title": "Cooling system for AI servers",
    "sector": "AI服务器液冷",
    "source": "agent-b"
  }
]
```

输出文件中会包含：
- `unique_candidates`
- `duplicate_candidates`
- `invalid_candidates`
- `stats`

## 设计重点

- 不修改 Hermes 现有逻辑
- 扫描现有知识库建立专利号级别索引
- 新候选记录必须先过索引去重
- 输出保存在 `~/Desktop/专利知识库/codex_workbench/`
- 通过标准 CLI 和 JSON 结果为其他 agent 提供稳定接口
