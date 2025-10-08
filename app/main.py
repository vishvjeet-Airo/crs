from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth as auth_router
from app.routers import upload as upload_router
from app.routers import query as query_router

app = FastAPI(
    title="Compass Risk Scanner API",
    version="0.1.0",
    description=(
        "Upload an Excel knowledge base with arbitrary columns including section and technology, "
        "then query with sections/technologies and top_k."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(upload_router.router, prefix="/upload", tags=["upload"])
app.include_router(query_router.router, prefix="/query", tags=["query"])


