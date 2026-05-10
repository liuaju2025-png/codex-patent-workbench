from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .config import ANALYSIS_DIR, INDEX_PATH, OCR_DONE_FILE, RAW_DIR, ensure_workbench_dirs
from .models import PatentOccurrence, PatentRecord
from .patent_id import extract_patent_id_from_text


def _guess_sector(path: Path, root: Path) -> str | None:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return None
    parts = rel.parts
    if len(parts) >= 2:
        return parts[0]
    return None


def _scan_tree(root: Path, kind: str) -> dict[str, PatentRecord]:
    records: dict[str, PatentRecord] = {}
    if not root.exists():
        return records

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        patent_id = extract_patent_id_from_text(path.name)
        if not patent_id:
            continue
        record = records.setdefault(patent_id, PatentRecord(patent_id=patent_id))
        record.add_occurrence(
            PatentOccurrence(
                patent_id=patent_id,
                path=str(path),
                kind=kind,
                sector=_guess_sector(path, root),
            )
        )
    return records


def _merge_records(*record_maps: dict[str, PatentRecord]) -> dict[str, PatentRecord]:
    merged: dict[str, PatentRecord] = {}
    for record_map in record_maps:
        for patent_id, record in record_map.items():
            target = merged.setdefault(patent_id, PatentRecord(patent_id=patent_id))
            for occurrence in record.occurrences:
                target.add_occurrence(occurrence)
    return merged


def _load_ocr_done_records() -> dict[str, PatentRecord]:
    records: dict[str, PatentRecord] = {}
    if not OCR_DONE_FILE.exists():
        return records

    data = json.loads(OCR_DONE_FILE.read_text(encoding="utf-8"))
    for path_str in data:
        path = Path(path_str)
        patent_id = extract_patent_id_from_text(path.name)
        if not patent_id:
            continue
        record = records.setdefault(patent_id, PatentRecord(patent_id=patent_id))
        record.add_occurrence(
            PatentOccurrence(
                patent_id=patent_id,
                path=path_str,
                kind="ocr_done",
                sector=_guess_sector(path, RAW_DIR),
            )
        )
    return records


def build_inventory_index() -> dict:
    ensure_workbench_dirs()

    raw_records = _scan_tree(RAW_DIR, "raw")
    analysis_records = _scan_tree(ANALYSIS_DIR, "analysis")
    ocr_records = _load_ocr_done_records()
    merged = _merge_records(raw_records, analysis_records, ocr_records)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "stats": {
            "unique_patents": len(merged),
            "raw_patents": len(raw_records),
            "analysis_patents": len(analysis_records),
            "ocr_patents": len(ocr_records),
        },
        "patents": {patent_id: record.to_dict() for patent_id, record in sorted(merged.items())},
    }

    INDEX_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def load_inventory_index() -> dict:
    if not INDEX_PATH.exists():
        return build_inventory_index()
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
