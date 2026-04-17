from fastapi import APIRouter
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import asyncio
from backend.rag.embeddings import (
    embed_all_existing_reviews,
    get_collection_count,
)
from backend.rag.chain import answer_question

router   = APIRouter(prefix="/rag", tags=["rag"])
executor = ThreadPoolExecutor(max_workers=2)

class QuestionRequest(BaseModel):
    question:  str
    n_results: int = 5

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    loop   = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        lambda: answer_question(request.question, request.n_results)
    )
    return result

@router.post("/index")
async def index_reviews():
    loop  = asyncio.get_event_loop()
    count = await loop.run_in_executor(
        executor,
        embed_all_existing_reviews
    )
    total = get_collection_count()
    return {
        "newly_indexed": count,
        "total_indexed": total,
        "status":        "ok"
    }

@router.get("/stats")
def rag_stats():
    return {
        "total_indexed": get_collection_count(),
        "status":        "ok"
    }