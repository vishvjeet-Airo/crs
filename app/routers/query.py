from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.schemas import MatchItem, QueryRequest, QueryResponse, User
from app.services.storage import data_store

router = APIRouter()


@router.post("/search", response_model=QueryResponse, summary="Query knowledge base with filters")
async def query_kb(payload: QueryRequest, current_user: User = Depends(get_current_user)) -> QueryResponse:
    results = data_store.search(
        sections=payload.sections,
        technologies=payload.technologies,
        top_k=payload.top_k,
    )

    items: List[MatchItem] = []
    for r in results:
        items.append(
            MatchItem(
                score=0.0,  # score hidden in this version; could be exposed later
                section=r.section,
                technology=r.technology,
                row_index=r.row_index,
                row={k: ("" if v is None else v) for k, v in r.row.items()},
            )
        )

    return QueryResponse(
        question=payload.question,
        top_k=payload.top_k,
        results=items,
        generated_at=datetime.now(timezone.utc),
    )
