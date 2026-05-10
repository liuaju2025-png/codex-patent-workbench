from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from codex_patent_workbench.dedup import filter_candidates
from codex_patent_workbench.patent_id import extract_patent_id_from_text, normalize_patent_id


class PatentIdTest(unittest.TestCase):
    def test_normalize_patent_id(self) -> None:
        self.assertEqual(normalize_patent_id("us20250012345a1"), "US20250012345A1")
        self.assertEqual(normalize_patent_id(" CN-118302107A "), "CN118302107A")
        self.assertIsNone(normalize_patent_id("not-a-patent"))

    def test_extract_patent_id_from_text(self) -> None:
        text = "Read patent WO2026999999A1 for packaging details"
        self.assertEqual(extract_patent_id_from_text(text), "WO2026999999A1")


class DedupTest(unittest.TestCase):
    def test_filter_candidates(self) -> None:
        candidates = [
            {"patent_id": "CN118302107A", "title": "already exists"},
            {"patent_id": "US20250012345A1", "title": "new patent"},
            {"patent_id": "us20250012345a1", "title": "batch duplicate"},
            {"title": "WO2026999999A1 embedded in title"},
            {"title": "missing id"},
        ]

        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "candidates.json"
            input_path.write_text(json.dumps(candidates, ensure_ascii=False), encoding="utf-8")

            fake_inventory = {"patents": {"CN118302107A": {"patent_id": "CN118302107A"}}}
            with patch("codex_patent_workbench.dedup.load_inventory_index", return_value=fake_inventory):
                with patch("codex_patent_workbench.dedup.FILTER_OUTPUT_DIR", Path(tmp)):
                    payload = filter_candidates(input_path)

        self.assertEqual(payload["stats"]["total_candidates"], 5)
        self.assertEqual(payload["stats"]["unique_candidates"], 2)
        self.assertEqual(payload["stats"]["duplicate_candidates"], 2)
        self.assertEqual(payload["stats"]["invalid_candidates"], 1)


if __name__ == "__main__":
    unittest.main()
