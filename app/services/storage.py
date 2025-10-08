from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


@dataclass
class IndexedRow:
    row: Dict[str, Any]
    section: Optional[str]
    technology: Optional[str]
    sheet: str
    source_filename: str
    row_index: int


class InMemoryDataStore:
    def __init__(self) -> None:
        self._rows: List[IndexedRow] = []

    def add_row(
        self,
        record: Dict[str, Any],
        sheet_name: str,
        section_column: Optional[str],
        technology_column: Optional[str],
        source_filename: str,
        row_index: int,
    ) -> None:
        section_value = _to_text(record.get(section_column)) if section_column else None
        technology_value = _to_text(record.get(technology_column)) if technology_column else None
        self._rows.append(
            IndexedRow(
                row=record,
                section=section_value,
                technology=technology_value,
                sheet=sheet_name,
                source_filename=source_filename,
                row_index=row_index,
            )
        )

    def count_rows(self) -> int:
        return len(self._rows)

    def search(
        self,
        sections: Optional[List[str]],
        technologies: Optional[List[str]],
        top_k: int,
    ) -> List[IndexedRow]:
        if not self._rows:
            return []

        def score_row(item: IndexedRow) -> float:
            score = 0.0
            if sections:
                for s in sections:
                    s_norm = s.lower()
                    if item.section:
                        val = item.section.lower()
                        if s_norm == val:
                            score += 2.0
                        elif s_norm in val or val in s_norm:
                            score += 1.0
            if technologies:
                for t in technologies:
                    t_norm = t.lower()
                    if item.technology:
                        val = item.technology.lower()
                        if t_norm == val:
                            score += 2.0
                        elif t_norm in val or val in t_norm:
                            score += 1.0
            return score

        scored = [(score_row(r), r) for r in self._rows]
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [r for s, r in scored if s > 0][:top_k]
        return results


data_store = InMemoryDataStore()
