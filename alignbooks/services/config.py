"""Company configuration services."""

from __future__ import annotations

from typing import Any

from ._base import BaseService


class ConfigService(BaseService):
    """Configuration operations."""

    def get_company_setup(self) -> dict[str, Any]:
        """Get company setup details."""
        return self._call("Display_CompanySetup", service="ABConfigurationService.svc")

    def get_document_numbering(self) -> dict[str, Any]:
        """Get document numbering configuration."""
        return self._call("Display_DocumentNumberingSetup", service="ABConfigurationService.svc")
