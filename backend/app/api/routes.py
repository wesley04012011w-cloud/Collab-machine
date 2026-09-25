from typing import Any

from fastapi import APIRouter, HTTPException

from ..services.colab import colab_service
from ..services.ollama import ollama_service

router = APIRouter()


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "backend": "online",
        "colab_api_enabled": colab_service.enabled,
        "ollama_url": ollama_service.base_url,
    }


@router.get("/colab/runtimes")
async def list_runtimes() -> dict[str, Any]:
    try:
        return {"runtimes": await colab_service.list_runtimes()}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/colab/runtimes")
async def create_runtime() -> dict[str, Any]:
    try:
        return {"runtime": await colab_service.create_runtime()}
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.delete("/colab/runtimes/{runtime_id}")
async def delete_runtime(runtime_id: str) -> dict[str, Any]:
    try:
        await colab_service.delete_runtime(runtime_id)
        return {"ok": True}
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/ollama/status")
async def ollama_status() -> dict[str, Any]:
    return await ollama_service.status()


@router.get("/ollama/models")
async def ollama_models() -> dict[str, Any]:
    return await ollama_service.models()


@router.post("/ollama/show")
async def ollama_show(payload: dict[str, Any]) -> dict[str, Any]:
    model = str(payload.get("model", "")).strip()
    if not model:
        raise HTTPException(status_code=400, detail="model is required")
    try:
        return await ollama_service.show(model)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/ollama/chat")
async def ollama_chat(payload: dict[str, Any]) -> dict[str, Any]:
    if not payload.get("model"):
        raise HTTPException(status_code=400, detail="model is required")
    if not isinstance(payload.get("messages"), list):
        raise HTTPException(status_code=400, detail="messages must be a list")
    try:
        return await ollama_service.chat(payload)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/ollama/generate")
async def ollama_generate(payload: dict[str, Any]) -> dict[str, Any]:
    if not payload.get("model"):
        raise HTTPException(status_code=400, detail="model is required")
    try:
        return await ollama_service.generate(payload)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/ollama/pull")
async def ollama_pull(payload: dict[str, Any]) -> dict[str, Any]:
    model = str(payload.get("model", "")).strip()
    if not model:
        raise HTTPException(status_code=400, detail="model is required")
    try:
        return await ollama_service.pull(model)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
