from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.dependencies import rag_engine


router = APIRouter(
    prefix="/api",
    tags=["Indexing"]
)


@router.post("/index")
async def index_code(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    if not file.filename.endswith(".py"):
        raise HTTPException(
            status_code=400,
            detail="Currently only Python files are supported"
        )

    content = await file.read()

    try:
        code = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoded"
        )

    try:

        result = rag_engine.index_code(
            code,
            file.filename
        )

        return {
            "filename": file.filename,
            **result
        }

    except SyntaxError as error:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid Python syntax: {error}"
        )