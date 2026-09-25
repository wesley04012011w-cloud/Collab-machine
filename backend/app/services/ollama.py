from __future__ import annotations

from typing import Any, AsyncIterator
import json

import httpx

from ..settings import settings


class OllamaService:
    def __init__(self) -> None:
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.token = settings.ollama_token.strip()

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    async def status(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags", headers=self._headers())
                response.raise_for_status()
            return {"online": True, "url": self.base_url}
        except (httpx.HTTPError, OSError) as exc:
            return {"online": False, "url": self.base_url, "error": str(exc)}

    async def models(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(f"{self.base_url}/api/tags", headers=self._headers())
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, OSError) as exc:
            return {"models": [], "error": str(exc)}

    async def show(self, model: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"{self.base_url}/api/show",
                headers=self._headers(),
                json={"name": model},
            )
            response.raise_for_status()
            return response.json()

    async def chat(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = dict(payload)
        body.setdefault("stream", False)
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                headers=self._headers(),
                json=body,
            )
            response.raise_for_status()
            return response.json()

    async def pull(self, model: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=1800) as client:
            response = await client.post(
                f"{self.base_url}/api/pull",
                headers=self._headers(),
                json={"name": model, "stream": False},
            )
            response.raise_for_status()
            return response.json()

    async def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = dict(payload)
        body.setdefault("stream", False)
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                headers=self._headers(),
                json=body,
            )
            response.raise_for_status()
            return response.json()


ollama_service = OllamaService()
