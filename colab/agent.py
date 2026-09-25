from __future__ import annotations

import os
import subprocess
from typing import Any

import httpx
from fastapi import FastAPI, Header, HTTPException

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
TOKEN = os.getenv("OLLAMA_STUDIO_TOKEN", "")

app = FastAPI(title="Collab Machine Colab Agent")


def auth(value: str | None) -> None:
    if TOKEN and value != f"Bearer {TOKEN}":
        raise HTTPException(status_code=401, detail="invalid token")


async def proxy(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.request(method, f"{OLLAMA_URL}{path}", json=payload)
        response.raise_for_status()
        return response.json()


@app.get("/")
async def root() -> dict[str, Any]:
    return {"ok": True, "service": "collab-machine-agent", "ollama_url": OLLAMA_URL}


@app.get("/health")
async def health(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    auth(authorization)
    try:
        data = await proxy("GET", "/api/tags")
        return {"ok": True, "ollama": True, "models": len(data.get("models", []))}
    except Exception as exc:
        return {"ok": True, "ollama": False, "error": str(exc)}


@app.get("/gpu")
async def gpu(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    auth(authorization)
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,utilization.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, check=True, timeout=5,
        )
        return {"online": True, "raw": result.stdout.strip()}
    except Exception as exc:
        return {"online": False, "error": str(exc)}


@app.get("/api/tags")
async def tags(authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("GET", "/api/tags")


@app.post("/api/show")
async def show(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("POST", "/api/show", payload)


@app.post("/api/chat")
async def chat(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("POST", "/api/chat", payload)


@app.post("/api/generate")
async def generate(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("POST", "/api/generate", payload)


@app.post("/api/pull")
async def pull(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("POST", "/api/pull", payload)


# Compatibility layer: the Android app can point directly at this agent
# and use the same /api/v1/... paths as the central backend.
@app.get("/api/v1/status")
async def api_status(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    auth(authorization)
    return {"backend": "agent", "colab_api_enabled": False, "ollama_url": OLLAMA_URL}


@app.get("/api/v1/ollama/status")
async def api_ollama_status(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    auth(authorization)
    try:
        data = await proxy("GET", "/api/tags")
        return {"online": True, "models": len(data.get("models", []))}
    except Exception as exc:
        return {"online": False, "error": str(exc)}


@app.get("/api/v1/ollama/models")
async def api_ollama_models(authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("GET", "/api/tags")


@app.post("/api/v1/ollama/show")
async def api_ollama_show(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("POST", "/api/show", payload)


@app.post("/api/v1/ollama/chat")
async def api_ollama_chat(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("POST", "/api/chat", payload)


@app.post("/api/v1/ollama/generate")
async def api_ollama_generate(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("POST", "/api/generate", payload)


@app.post("/api/v1/ollama/pull")
async def api_ollama_pull(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> Any:
    auth(authorization)
    return await proxy("POST", "/api/pull", payload)
