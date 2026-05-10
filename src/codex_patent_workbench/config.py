import os
from pathlib import Path


def _path_from_env(name: str, default: Path) -> Path:
    value = os.environ.get(name)
    return Path(value).expanduser() if value else default


BASE_DIR = _path_from_env("PATENT_WORKBENCH_BASE_DIR", Path.home() / "Desktop" / "专利知识库")
RAW_DIR = _path_from_env("PATENT_WORKBENCH_RAW_DIR", BASE_DIR / "专利原文")
ANALYSIS_DIR = _path_from_env("PATENT_WORKBENCH_ANALYSIS_DIR", BASE_DIR / "专利分析报告")
LOGS_DIR = _path_from_env("PATENT_WORKBENCH_LOGS_DIR", BASE_DIR / "logs")
OCR_DONE_FILE = _path_from_env("PATENT_WORKBENCH_OCR_DONE_FILE", LOGS_DIR / "patent_ocr_done.json")
WORKBENCH_DIR = _path_from_env("PATENT_WORKBENCH_OUTPUT_DIR", BASE_DIR / "codex_workbench")
INDEX_PATH = WORKBENCH_DIR / "patent_inventory_index.json"
FILTER_OUTPUT_DIR = WORKBENCH_DIR / "filter_runs"


def ensure_workbench_dirs() -> None:
    WORKBENCH_DIR.mkdir(parents=True, exist_ok=True)
    FILTER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
