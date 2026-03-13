from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from backend.app.search.hybrid import HybridSearch

router = APIRouter()

search_engine = HybridSearch()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    alpha: float = 0.5


class SearchResult(BaseModel):
    doc_id: str
    title: str
    bm25_score: float
    vector_score: float
    hybrid_score: float


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/search", response_model=List[SearchResult])
def search(request: SearchRequest):

    results = search_engine.search(
        request.query,
        request.top_k
    )

    return results