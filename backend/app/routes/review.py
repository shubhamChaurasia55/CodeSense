from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.code_analyzer import analyze_python_code
from app.services.dependencies import rag_engine
from app.services.review_prompt import build_review_prompt


router = APIRouter(
    prefix="/api",
    tags=["Review"]
)


@router.post("/review")
async def review_code(file: UploadFile = File(...)):

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
        analysis = analyze_python_code(code)
    except SyntaxError as error:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Python syntax: {error}"
        )

    prompt = build_review_prompt(
        code,
        analysis
    )

    try:
        review = rag_engine.llm.review(prompt)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI review failed: {error}"
        )

    return {
        "filename": file.filename,
        "function_count": len(analysis),
        "analysis": analysis,
        "review": review.model_dump()
    }