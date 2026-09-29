from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.code_analyzer import analyze_python_code

router = APIRouter(prefix="/api", tags=["Analyze"])


@router.post("/analyze")
async def analyze_code(file: UploadFile = File(...)):
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
        results = analyze_python_code(code)
    except SyntaxError as error:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Python syntax: {error}"
        )

    return {
        "filename": file.filename,
        "function_count": len(results),
        "functions": results
    }