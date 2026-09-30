from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes.indexing import router as indexing_router
from app.routes.query import router as query_router
from app.routes.ask import router as ask_router
from app.routes.debug import router as debug_router
from app.routes.analyze import router as analyze_router
from app.routes.review import router as review_router
from app.routes.project import router as project_router


app = FastAPI(
    title="CodeSense",
    description="AI Code Intelligence & Debugging Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(indexing_router)
app.include_router(query_router)
app.include_router(ask_router)
app.include_router(debug_router)
app.include_router(analyze_router)
app.include_router(review_router)
app.include_router(project_router)


@app.get("/")
def root():
    return {"message": "CodeSense API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}