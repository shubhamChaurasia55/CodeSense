from fastapi import FastAPI

from app.routes.upload import router as upload_router
from app.routes.indexing import router as indexing_router
from app.routes.query import router as query_router
from app.routes.ask import router as ask_router


app = FastAPI(
    title="CodeSense",
    description="AI Code Intelligence & Debugging Assistant",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(indexing_router)
app.include_router(query_router)
app.include_router(ask_router)


@app.get("/")
def root():
    return {"message": "CodeSense API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}