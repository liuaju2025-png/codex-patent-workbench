from __future__ import annotations

import re


PATENT_ID_PATTERN = re.compile(r"(?:CN|US|EP|WO|JP|KR)[0-9A-Z]+", re.IGNORECASE)


def normalize_patent_id(value: str | None) -> str | None:
    if not value:
        return None
    compact = re.sub(r"[\s_\\-]+", "", value).upper()
    match = PATENT_ID_PATTERN.search(compact)
    if match:
        return match.group(0).upper()
    return None


def extract_patent_id_from_text(value: str | None) -> str | None:
    if not value:
        return None
    match = PATENT_ID_PATTERN.search(value.upper())
    if match:
        return match.group(0).upper()
    return None
