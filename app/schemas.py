from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    disabled: bool = False


class UploadResponse(BaseModel):
    filename: str
    worksheets_loaded: int
    rows_indexed: int
    inferred_columns: Dict[str, Optional[str]] = Field(
        description="Mapping of logical fields to detected sheet column names"
    )


class QueryRequest(BaseModel):
    question: str = Field(description="Natural-language question to answer")
    sections: Optional[List[str]] = Field(
        default=None, description="Candidate sections to match (partial or exact)"
    )
    technologies: Optional[List[str]] = Field(
        default=None, description="Candidate technologies to match (partial or exact)"
    )
    top_k: int = Field(
        default=5, ge=1, le=50, description="Max results to return based on match"
    )


class MatchItem(BaseModel):
    score: float
    section: Optional[str] = None
    technology: Optional[str] = None
    row_index: int
    row: Dict[str, Any]


class QueryResponse(BaseModel):
    question: str
    top_k: int
    results: List[MatchItem]
    generated_at: datetime
