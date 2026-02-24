"""Inventory management services: stock transfers, adjustments."""

from __future__ import annotations

from typing import Any

from ..constants import VType
from ._base import BaseService


class InventoryService(BaseService):
    """Inventory and stock operations."""

    def list_adjustments(
        self,
        from_date: str = "",
        to_date: str = "",
    ) -> list[dict[str, Any]]:
        """List material adjustments."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": "",
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.MATERIAL_ADJUSTMENT,
            }
        })
        return result if isinstance(result, list) else []

    def get_adjustment(self, adjustment_id: str) -> dict[str, Any]:
        """Get material adjustment details."""
        return self._call("Display_MaterialAdjustment", {
            "id": adjustment_id,
            "vtype": VType.MATERIAL_ADJUSTMENT,
        })
