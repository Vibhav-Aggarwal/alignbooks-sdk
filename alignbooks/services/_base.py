"""Base service class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import AlignBooksClient


class BaseService:
    """Base class for all service modules."""

    def __init__(self, client: AlignBooksClient):
        self._client = client

    def _call(self, endpoint: str, body: dict[str, Any] | None = None, **kwargs) -> Any:
        return self._client.api_call(endpoint, body, **kwargs)
