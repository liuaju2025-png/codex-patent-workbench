from pathlib import Path


BASE_DIR = Path.home() / "Desktop" / "专利知识库"
RAW_DIR = BASE_DIR / "专利原文"
ANALYSIS_DIR = BASE_DIR / "专利分析报告"
LOGS_DIR = BASE_DIR / "logs"
OCR_DONE_FILE = LOGS_DIR / "patent_ocr_done.json"
WORKBENCH_DIR = BASE_DIR / "codex_workbench"
INDEX_PATH = WORKBENCH_DIR / "patent_inventory_index.json"
FILTER_OUTPUT_DIR = WORKBENCH_DIR / "filter_runs"


def ensure_workbench_dirs() -> None:
    WORKBENCH_DIR.mkdir(parents=True, exist_ok=True)
    FILTER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
