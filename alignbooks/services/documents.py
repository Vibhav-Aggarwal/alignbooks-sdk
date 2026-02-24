"""Document utility services: PDF, delete, etc."""

from __future__ import annotations

from typing import Any

from ._base import BaseService


class DocumentsService(BaseService):
    """Document utility operations."""

    def delete(self, doc_id: str, vtype: int) -> dict[str, Any]:
        """Delete a document by ID and VType.

        Args:
            doc_id: Document ID (GUID).
            vtype: Document type (VType constant).

        Returns:
            API response indicating success or failure.
        """
        return self._call("Delete_Document", {
            "id": doc_id,
            "master_type": vtype,
        })

    def get_pdf(self, doc_id: str, vtype: int, format_id: str = "") -> tuple[bytes, str]:
        """Generate and return PDF bytes for a document.

        Args:
            doc_id: Document ID (GUID).
            vtype: Document type (VType constant).
            format_id: Print format ID (optional).

        Returns:
            Tuple of (pdf_bytes, filename).
        """
        return self._client.get_pdf(doc_id, vtype, format_id)
