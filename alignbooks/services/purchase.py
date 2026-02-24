"""Purchase services: bills, purchase orders, GRN."""

from __future__ import annotations

from typing import Any

from ..constants import VType
from ..models import ItemDetail, build_document_shell
from ._base import BaseService


class PurchaseService(BaseService):
    """Purchase document operations."""

    # --- Purchase Bills ---

    def list_bills(
        self,
        from_date: str = "",
        to_date: str = "",
        location_id: str = "",
    ) -> list[dict[str, Any]]:
        """List purchase bills.

        Note: AlignBooks server may ignore date filters; results are filtered client-side.

        Args:
            from_date: Start date (YYYY-MM-DD).
            to_date: End date (YYYY-MM-DD).
            location_id: Branch/location ID filter.

        Returns:
            List of purchase bill summaries.
        """
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": location_id,
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.PURCHASE_BILL,
            }
        })
        return result if isinstance(result, list) else []

    def get_bill(self, bill_id: str) -> dict[str, Any]:
        """Get full purchase bill details.

        Args:
            bill_id: Bill document ID (GUID).

        Returns:
            Complete bill data including items, taxes, etc.
        """
        return self._call("Display_Invoice", {
            "id": bill_id,
            "vtype": VType.PURCHASE_BILL,
        })

    def create_bill(
        self,
        bill_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a purchase bill.

        IMPORTANT: Uses body key "invoice" (NOT "info").

        Args:
            bill_data: Complete bill structure (use build_document_shell() as base).

        Returns:
            API response with IDValue of created bill.

        Example:
            >>> from alignbooks.models import build_document_shell, ItemDetail
            >>> bill = build_document_shell(
            ...     party_id="vendor-guid",
            ...     vdate="2026-02-24 00:00:00",
            ...     ref_no="INV-001",
            ... )
            >>> item = ItemDetail(item_id="item-guid", qty=10, rate=100, tax_rate=18)
            >>> bill["item_detail"] = [item.to_api_dict()]
            >>> result = ab.purchase.create_bill(bill)
        """
        return self._call("SaveUpdate_Invoice", {
            "is_new_mode": True,
            "invoice": bill_data,
            "vtype": VType.PURCHASE_BILL,
        })

    def update_bill(self, bill_data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing purchase bill."""
        return self._call("SaveUpdate_Invoice", {
            "is_new_mode": False,
            "invoice": bill_data,
            "vtype": VType.PURCHASE_BILL,
        })

    # --- Purchase Orders ---

    def list_orders(
        self,
        from_date: str = "",
        to_date: str = "",
        location_id: str = "",
    ) -> list[dict[str, Any]]:
        """List purchase orders.

        Args:
            from_date: Start date (YYYY-MM-DD).
            to_date: End date (YYYY-MM-DD).
            location_id: Branch/location ID filter.

        Returns:
            List of purchase order summaries.
        """
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": location_id,
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.PURCHASE_ORDER,
            }
        })
        return result if isinstance(result, list) else []

    def get_order(self, order_id: str) -> dict[str, Any]:
        """Get full purchase order details.

        Args:
            order_id: PO document ID (GUID).
        """
        return self._call("Display_Order", {
            "id": order_id,
            "vtype": VType.PURCHASE_ORDER,
        })

    def create_order(
        self,
        order_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a purchase order.

        Uses body key "info" (different from bills which use "invoice").

        Args:
            order_data: Complete order structure (use build_document_shell() as base).

        Returns:
            API response with IDValue of created PO.
        """
        return self._call("SaveUpdate_Order", {
            "is_new_mode": True,
            "info": order_data,
            "vtype": VType.PURCHASE_ORDER,
        })

    def update_order(self, order_data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing purchase order."""
        return self._call("SaveUpdate_Order", {
            "is_new_mode": False,
            "info": order_data,
            "vtype": VType.PURCHASE_ORDER,
        })

    # --- GRN ---

    def list_grn(
        self,
        from_date: str = "",
        to_date: str = "",
        location_id: str = "",
    ) -> list[dict[str, Any]]:
        """List Goods Receipt Notes."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": location_id,
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.GOODS_RECEIPT_NOTE,
            }
        })
        return result if isinstance(result, list) else []

    def get_grn(self, grn_id: str) -> dict[str, Any]:
        """Get GRN details."""
        return self._call("Display_Invoice", {
            "id": grn_id,
            "vtype": VType.GOODS_RECEIPT_NOTE,
        })

    # --- Purchase Returns ---

    def list_returns(
        self,
        from_date: str = "",
        to_date: str = "",
    ) -> list[dict[str, Any]]:
        """List purchase returns (debit notes)."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": "",
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.PURCHASE_RETURN,
            }
        })
        return result if isinstance(result, list) else []
