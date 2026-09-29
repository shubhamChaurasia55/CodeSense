from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.dependencies import rag_engine


router = APIRouter(
    prefix="/api",
    tags=["Debug"]
)


class DebugRequest(BaseModel):
    question: str
    top_k: int = 3


@router.post("/debug")
async def debug_code(request: DebugRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if not rag_engine.indexed:
        raise HTTPException(
            status_code=400,
            detail="No code has been indexed yet"
        )

    try:
        result = rag_engine.debug(
            request.question,
            request.top_k
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )