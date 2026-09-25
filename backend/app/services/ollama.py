from __future__ import annotations
from typing import Any
import httpx
from ..settings import settings

class OllamaService:
    def __init__(self) -> None:
        self.base_url = settings.ollama_base_url.rstrip("/")

    async def status(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
            return {"online": True}
        except (httpx.HTTPError, OSError) as exc:
            return {"online": False, "error": str(exc)}

    async def models(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, OSError) as exc:
            return {"models": [], "error": str(exc)}

ollama_service = OllamaService()
