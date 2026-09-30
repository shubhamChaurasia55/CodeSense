from fastapi import APIRouter

from app.services.dependencies import rag_engine


router = APIRouter(
    prefix="/api/project",
    tags=["Project"]
)


@router.post("/reset")
async def reset_project():
    return rag_engine.reset_project()