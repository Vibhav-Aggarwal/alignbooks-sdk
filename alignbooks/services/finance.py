"""Finance and accounting services: payments, receipts, journals."""

from __future__ import annotations

from typing import Any

from ..constants import VType
from ._base import BaseService


class FinanceService(BaseService):
    """Finance document operations."""

    def list_payments(
        self,
        from_date: str = "",
        to_date: str = "",
    ) -> list[dict[str, Any]]:
        """List payment vouchers."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": "",
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.PAYMENT_VOUCHER,
            }
        })
        return result if isinstance(result, list) else []

    def get_payment(self, payment_id: str) -> dict[str, Any]:
        """Get payment voucher details."""
        return self._call("Display_PaymentReceiptVoucher", {
            "id": payment_id,
            "vtype": VType.PAYMENT_VOUCHER,
        })

    def list_receipts(
        self,
        from_date: str = "",
        to_date: str = "",
    ) -> list[dict[str, Any]]:
        """List receipt vouchers."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": "",
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.RECEIPT_VOUCHER,
            }
        })
        return result if isinstance(result, list) else []

    def get_receipt(self, receipt_id: str) -> dict[str, Any]:
        """Get receipt voucher details."""
        return self._call("Display_PaymentReceiptVoucher", {
            "id": receipt_id,
            "vtype": VType.RECEIPT_VOUCHER,
        })

    def list_journals(
        self,
        from_date: str = "",
        to_date: str = "",
    ) -> list[dict[str, Any]]:
        """List journal vouchers."""
        result = self._call("List_Document", {
            "info": {
                "master_id": "",
                "branch_id": "",
                "from_date": from_date,
                "to_date": to_date,
                "master_type": VType.JOURNAL_VOUCHER,
            }
        })
        return result if isinstance(result, list) else []

    def get_journal(self, journal_id: str) -> dict[str, Any]:
        """Get journal voucher details."""
        return self._call("Display_JournalVoucher", {
            "id": journal_id,
            "vtype": VType.JOURNAL_VOUCHER,
        })
