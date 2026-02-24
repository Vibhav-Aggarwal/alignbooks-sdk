"""Master data services: vendors, customers, items, ledgers."""

from __future__ import annotations

from typing import Any

from ..constants import ZERO_GUID, MasterType
from ._base import BaseService


class MastersService(BaseService):
    """Generic master data operations using ShortList endpoint."""

    def shortlist(self, master_type: int) -> list[dict[str, Any]]:
        """Get a short list of master records.

        Args:
            master_type: MasterType constant (e.g. MasterType.VENDOR).

        Returns:
            List of master records with id, name, and other fields.
        """
        result = self._call("ShortList", {
            "new_id": ZERO_GUID,
            "master_type": master_type,
        })
        return result if isinstance(result, list) else []


class VendorsService(BaseService):
    """Vendor (supplier) operations."""

    def list(self) -> list[dict[str, Any]]:
        """List all vendors.

        Returns:
            List of vendor records.

        Example:
            >>> vendors = ab.vendors.list()
            >>> for v in vendors:
            ...     print(v["name"], v["id"])
        """
        result = self._call("ShortList", {
            "new_id": ZERO_GUID,
            "master_type": MasterType.VENDOR,
        })
        return result if isinstance(result, list) else []

    def get(self, vendor_id: str) -> dict[str, Any]:
        """Get detailed vendor/party information.

        Args:
            vendor_id: Vendor ID (GUID).

        Returns:
            Full vendor record from Display_Party.
        """
        return self._call("Display_Party", {"id": vendor_id})

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new vendor.

        Args:
            data: Vendor data dictionary matching AlignBooks Party structure.

        Returns:
            API response with IDValue of created vendor.
        """
        return self._call("SaveUpdate_Party", {
            "is_new_mode": True,
            "info": data,
        })

    def update(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing vendor.

        Args:
            data: Vendor data dictionary with 'id' field set.

        Returns:
            API response.
        """
        return self._call("SaveUpdate_Party", {
            "is_new_mode": False,
            "info": data,
        })

    def get_info(self, vendor_id: str, vtype: int = 18) -> dict[str, Any]:
        """Get party info for transaction context.

        Args:
            vendor_id: Vendor ID (GUID).
            vtype: Document type context (default 18 = Purchase Bill).

        Returns:
            Party info including addresses, GST, etc.
        """
        return self._call("GetPartyInfo", {
            "party_id": vendor_id,
            "vtype": vtype,
        })


class CustomersService(BaseService):
    """Customer operations."""

    def list(self) -> list[dict[str, Any]]:
        """List all customers.

        Returns:
            List of customer records.
        """
        result = self._call("ShortList", {
            "new_id": ZERO_GUID,
            "master_type": MasterType.CUSTOMER,
        })
        return result if isinstance(result, list) else []

    def get(self, customer_id: str) -> dict[str, Any]:
        """Get detailed customer information.

        Args:
            customer_id: Customer ID (GUID).
        """
        return self._call("Display_Party", {"id": customer_id})

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new customer."""
        return self._call("SaveUpdate_Party", {
            "is_new_mode": True,
            "info": data,
        })

    def update(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing customer."""
        return self._call("SaveUpdate_Party", {
            "is_new_mode": False,
            "info": data,
        })


class ItemsService(BaseService):
    """Item/product operations."""

    def list(self) -> list[dict[str, Any]]:
        """List all items.

        Returns:
            List of item records.

        Example:
            >>> items = ab.items.list()
            >>> for item in items:
            ...     print(item["name"], item.get("item_code"))
        """
        result = self._call("ShortList", {
            "new_id": ZERO_GUID,
            "master_type": MasterType.ITEM,
        })
        return result if isinstance(result, list) else []

    def get(self, item_id: str) -> dict[str, Any]:
        """Get detailed item information.

        Args:
            item_id: Item ID (GUID).
        """
        return self._call("Display_Item", {"id": item_id})

    def get_info(self, item_id: str, vtype: int = 18) -> dict[str, Any]:
        """Get item info for transaction context (rates, tax, stock).

        Args:
            item_id: Item ID (GUID).
            vtype: Document type context.
        """
        return self._call("GetItemInfo", {
            "item_id": item_id,
            "vtype": vtype,
        })

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new item."""
        return self._call("SaveUpdate_Item", {
            "is_new_mode": True,
            "item_information": data,
        })

    def update(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing item."""
        return self._call("SaveUpdate_Item", {
            "is_new_mode": False,
            "item_information": data,
        })

    def list_with_balance(self) -> list[dict[str, Any]]:
        """List items with stock balance."""
        result = self._call("ShortList_ItemWithBalance", {
            "new_id": ZERO_GUID,
        })
        return result if isinstance(result, list) else []


class LedgersService(BaseService):
    """Ledger/account operations."""

    def list(self) -> list[dict[str, Any]]:
        """List all ledgers."""
        result = self._call("ShortList", {
            "new_id": ZERO_GUID,
            "master_type": MasterType.LEDGER,
        })
        return result if isinstance(result, list) else []

    def get(self, ledger_id: str) -> dict[str, Any]:
        """Get detailed ledger information."""
        return self._call("Display_Ledger", {"id": ledger_id})

    def get_info(self, ledger_id: str) -> dict[str, Any]:
        """Get ledger info including group details."""
        return self._call("GetLedgerInfo", {"ledger_id": ledger_id})

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new ledger."""
        return self._call("SaveUpdate_Ledger", {
            "is_new_mode": True,
            "info": data,
        })
