from fastapi import APIRouter, HTTPException
from ..services.colab import colab_service
from ..services.ollama import ollama_service

router = APIRouter()

@router.get("/status")
async def status() -> dict:
    return {
        "backend": "online",
        "colab_api_enabled": colab_service.enabled,
        "ollama_url": ollama_service.base_url,
    }

@router.get("/colab/runtimes")
async def list_runtimes() -> dict:
    return {"runtimes": await colab_service.list_runtimes()}

@router.post("/colab/runtimes")
async def create_runtime() -> dict:
    try:
        return {"runtime": await colab_service.create_runtime()}
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc

@router.delete("/colab/runtimes/{runtime_id}")
async def delete_runtime(runtime_id: str) -> dict:
    try:
        await colab_service.delete_runtime(runtime_id)
        return {"ok": True}
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc

@router.get("/ollama/status")
async def ollama_status() -> dict:
    return await ollama_service.status()

@router.get("/ollama/models")
async def ollama_models() -> dict:
    return await ollama_service.models()
