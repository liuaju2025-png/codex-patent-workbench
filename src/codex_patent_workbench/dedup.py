from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import FILTER_OUTPUT_DIR, ensure_workbench_dirs
from .inventory import load_inventory_index
from .patent_id import extract_patent_id_from_text, normalize_patent_id


def _candidate_patent_id(item: dict[str, Any]) -> str | None:
    for key in ("patent_id", "patent_number", "id", "url", "title"):
        patent_id = normalize_patent_id(str(item.get(key))) if item.get(key) else None
        if patent_id:
            return patent_id
        patent_id = extract_patent_id_from_text(str(item.get(key))) if item.get(key) else None
        if patent_id:
            return patent_id
    return None


def filter_candidates(input_path: Path) -> dict[str, Any]:
    ensure_workbench_dirs()
    inventory = load_inventory_index()
    existing_patents = inventory.get("patents", {})

    candidates = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(candidates, list):
        raise ValueError("Candidate input must be a JSON list.")

    seen_in_batch: set[str] = set()
    unique_candidates: list[dict[str, Any]] = []
    duplicate_candidates: list[dict[str, Any]] = []
    invalid_candidates: list[dict[str, Any]] = []

    for item in candidates:
        if not isinstance(item, dict):
            invalid_candidates.append({"reason": "not_an_object", "raw": item})
            continue

        patent_id = _candidate_patent_id(item)
        if not patent_id:
            invalid_candidates.append({"reason": "missing_patent_id", "raw": item})
            continue

        enriched = dict(item)
        enriched["normalized_patent_id"] = patent_id

        if patent_id in existing_patents:
            enriched["duplicate_reason"] = "already_in_knowledge_base"
            duplicate_candidates.append(enriched)
            continue

        if patent_id in seen_in_batch:
            enriched["duplicate_reason"] = "duplicate_within_batch"
            duplicate_candidates.append(enriched)
            continue

        seen_in_batch.add(patent_id)
        unique_candidates.append(enriched)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "input_file": str(input_path),
        "stats": {
            "total_candidates": len(candidates),
            "unique_candidates": len(unique_candidates),
            "duplicate_candidates": len(duplicate_candidates),
            "invalid_candidates": len(invalid_candidates),
            "existing_patents_in_inventory": len(existing_patents),
        },
        "unique_candidates": unique_candidates,
        "duplicate_candidates": duplicate_candidates,
        "invalid_candidates": invalid_candidates,
    }

    run_name = f"filter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = FILTER_OUTPUT_DIR / run_name
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    payload["output_file"] = str(output_path)
    return payload
