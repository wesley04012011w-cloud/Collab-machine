from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import settings
from .api.routes import router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Mobile control plane for Google Colab + Ollama.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict:
    return {"ok": True, "service": settings.app_name, "env": settings.app_env}
