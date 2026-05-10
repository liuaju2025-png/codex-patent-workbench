from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class PatentOccurrence:
    patent_id: str
    path: str
    kind: str
    sector: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PatentRecord:
    patent_id: str
    sectors: list[str] = field(default_factory=list)
    occurrences: list[PatentOccurrence] = field(default_factory=list)

    def add_occurrence(self, occurrence: PatentOccurrence) -> None:
        if occurrence.sector and occurrence.sector not in self.sectors:
            self.sectors.append(occurrence.sector)
        self.occurrences.append(occurrence)

    def to_dict(self) -> dict[str, Any]:
        return {
            "patent_id": self.patent_id,
            "sectors": sorted(self.sectors),
            "occurrence_count": len(self.occurrences),
            "occurrences": [item.to_dict() for item in self.occurrences],
        }
