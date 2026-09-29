from fastapi import FastAPI

from app.routes.upload import router as upload_router


app = FastAPI(
    title="CodeSense",
    description="AI Code Intelligence & Debugging Assistant",
    version="1.0.0"
)


app.include_router(upload_router)


@app.get("/")
def root():
    return {
        "message": "CodeSense API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }