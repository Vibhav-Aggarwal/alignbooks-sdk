"""Sales services: invoices, sales orders, estimates."""

from __future__ import annotations

from typing import Any

from ..constants import VType
from ..models import ItemDetail, build_document_shell
from ._base import BaseService


class SalesService(BaseService):
    """Sales document operations."""

    # --- Sales Invoices ---

    def list_invoices(
        self,
        from_date: str = "",
        to_date: str = "",
        location_id: str = "",
    ) -> list[dict[str, Any]]:
        """List sales invoices."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": location_id,
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.SALES_INVOICE,
            }
        })
        return result if isinstance(result, list) else []

    def get_invoice(self, invoice_id: str) -> dict[str, Any]:
        """Get full sales invoice details."""
        return self._call("Display_Invoice", {
            "id": invoice_id,
            "vtype": VType.SALES_INVOICE,
        })

    def create_invoice(self, invoice_data: dict[str, Any]) -> dict[str, Any]:
        """Create a sales invoice.

        IMPORTANT: Uses body key "invoice".
        """
        return self._call("SaveUpdate_Invoice", {
            "is_new_mode": True,
            "invoice": invoice_data,
            "vtype": VType.SALES_INVOICE,
        })

    def update_invoice(self, invoice_data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing sales invoice."""
        return self._call("SaveUpdate_Invoice", {
            "is_new_mode": False,
            "invoice": invoice_data,
            "vtype": VType.SALES_INVOICE,
        })

    # --- Sales Orders ---

    def list_orders(
        self,
        from_date: str = "",
        to_date: str = "",
        location_id: str = "",
    ) -> list[dict[str, Any]]:
        """List sales orders."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": location_id,
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.SALES_ORDER,
            }
        })
        return result if isinstance(result, list) else []

    def get_order(self, order_id: str) -> dict[str, Any]:
        """Get full sales order details."""
        return self._call("Display_Order", {
            "id": order_id,
            "vtype": VType.SALES_ORDER,
        })

    def create_order(self, order_data: dict[str, Any]) -> dict[str, Any]:
        """Create a sales order.

        Uses body key "info".
        """
        return self._call("SaveUpdate_Order", {
            "is_new_mode": True,
            "info": order_data,
            "vtype": VType.SALES_ORDER,
        })

    def update_order(self, order_data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing sales order."""
        return self._call("SaveUpdate_Order", {
            "is_new_mode": False,
            "info": order_data,
            "vtype": VType.SALES_ORDER,
        })

    # --- Estimates ---

    def list_estimates(
        self,
        from_date: str = "",
        to_date: str = "",
        location_id: str = "",
    ) -> list[dict[str, Any]]:
        """List sales estimates."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": location_id,
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.SALES_ESTIMATE,
            }
        })
        return result if isinstance(result, list) else []

    def get_estimate(self, estimate_id: str) -> dict[str, Any]:
        """Get estimate details."""
        return self._call("Display_Estimate", {
            "id": estimate_id,
            "vtype": VType.SALES_ESTIMATE,
        })

    def create_estimate(self, estimate_data: dict[str, Any]) -> dict[str, Any]:
        """Create a sales estimate.

        Uses body key "info".
        """
        return self._call("SaveUpdate_Estimate", {
            "is_new_mode": True,
            "info": estimate_data,
            "vtype": VType.SALES_ESTIMATE,
        })
