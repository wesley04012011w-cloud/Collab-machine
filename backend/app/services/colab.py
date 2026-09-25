from __future__ import annotations
from typing import Any
from ..settings import settings

class ColabService:
    def __init__(self) -> None:
        self.enabled = settings.colab_api_enabled

    async def list_runtimes(self) -> list[dict[str, Any]]:
        if not self.enabled:
            return []
        raise NotImplementedError("Colab API adapter is not configured yet.")

    async def create_runtime(self) -> dict[str, Any]:
        if not self.enabled:
            raise NotImplementedError("Enable COLAB_API_ENABLED after Google OAuth is configured.")
        raise NotImplementedError("Runtime creation is the next integration step.")

    async def delete_runtime(self, runtime_id: str) -> None:
        if not self.enabled:
            raise NotImplementedError("Enable COLAB_API_ENABLED after Google OAuth is configured.")
        raise NotImplementedError("Runtime deletion is the next integration step.")

colab_service = ColabService()
