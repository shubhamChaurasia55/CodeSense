from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.dependencies import rag_engine


router = APIRouter(
    prefix="/api",
    tags=["Query"]
)


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


@router.post("/query")
async def query_code(request: QueryRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:

        results = rag_engine.search(
            request.question,
            request.top_k
        )

        return {
            "question": request.question,
            "results": results
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )