from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.parser import parse_python_code

router = APIRouter(
    prefix="/api",
    tags=["Upload"]
)


ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".hpp"
}


@router.post("/upload")
async def upload_code(file: UploadFile = File(...)):

    filename = file.filename

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    extension = "." + filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    content = await file.read()

    try:
        code = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoded text"
        )

    return {
        "filename": filename,
        "extension": extension,
        "size_bytes": len(content),
        "lines": len(code.splitlines()),
        "code": code
    }


@router.post("/parse")
async def parse_code(file: UploadFile = File(...)):

    filename = file.filename

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    if not filename.endswith(".py"):
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
            detail="File must be UTF-8 encoded text"
        )

    try:
        chunks = parse_python_code(code)
    except SyntaxError as error:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Python syntax: {error}"
        )

    return {
        "filename": filename,
        "chunk_count": len(chunks),
        "chunks": chunks
    }