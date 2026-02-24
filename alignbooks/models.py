"""Data models for AlignBooks SDK.

Provides dataclass-based models for common AlignBooks entities with smart defaults.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from .constants import ZERO_GUID


def _new_guid() -> str:
    return str(uuid.uuid4())


def _id_name(id: str = "", name: str = "") -> dict[str, str]:
    """Create an {id, name} reference object."""
    return {"id": id, "name": name}


@dataclass
class ItemDetail:
    """A line item in an invoice, order, or bill.

    Attributes:
        item_id: Item master ID (GUID).
        item_name: Item display name.
        unit_id: Unit of measurement ID.
        unit_name: Unit name (e.g. 'PCS', 'KG').
        qty: Quantity.
        rate: Rate per unit.
        tax_rate: GST tax rate (e.g. 18 for 18%).
        hsn_code: HSN/SAC code for GST.
        description: Print description override.
        posting_gl_id: Posting ledger ID override.
        posting_gl_name: Posting ledger name.
    """

    item_id: str
    item_name: str = ""
    unit_id: str = ""
    unit_name: str = ""
    qty: float = 1
    rate: float = 0
    tax_rate: float = 0
    hsn_code: str = ""
    description: str = ""
    posting_gl_id: str = ""
    posting_gl_name: str = ""
    tax_id: str = ""
    tax_name: str = ""
    warehouse_id: str = ""
    warehouse_name: str = ""

    def to_api_dict(self, *, is_inter_state: bool = False) -> dict[str, Any]:
        """Convert to the API's AbItemDetail structure.

        Args:
            is_inter_state: If True, applies IGST; otherwise CGST+SGST.

        Returns:
            Dictionary matching the AlignBooks item detail format.
        """
        amount = self.qty * self.rate
        taxable = amount
        tax_amount = round(taxable * self.tax_rate / 100, 2)

        if is_inter_state:
            igst_rate = self.tax_rate
            igst_amount = tax_amount
            cgst_rate = sgst_rate = 0.0
            cgst_amount = sgst_amount = 0.0
        else:
            cgst_rate = sgst_rate = self.tax_rate / 2
            cgst_amount = round(taxable * cgst_rate / 100, 2)
            sgst_amount = round(taxable * sgst_rate / 100, 2)
            igst_rate = igst_amount = 0.0

        return {
            "id": _new_guid(),
            "item": _id_name(self.item_id, self.item_name),
            "sub_item": _id_name(),
            "sales_return": 0,
            "ri_tag": 0,
            "print_description": self.description or self.item_name,
            "unit": _id_name(self.unit_id, self.unit_name),
            "gross": 0,
            "bundle_qty": 0,
            "tare": 0,
            "qty": self.qty,
            "free_qty": 0,
            "pack_unit": _id_name(),
            "grand_pack_unit": _id_name(),
            "grand_pack_qty": 0,
            "pack_qty": 0,
            "rate": self.rate,
            "amount": amount,
            "tax": _id_name(self.tax_id, self.tax_name),
            "taxable": taxable,
            "tax_amount": tax_amount,
            "tax_rate": self.tax_rate,
            "cess_rate": 0,
            "cess_amount": 0,
            "igst_ledger": _id_name(),
            "igst_tax_amount": igst_amount,
            "igst_tax_rate": igst_rate,
            "cgst_ledger": _id_name(),
            "cgst_tax_amount": cgst_amount,
            "cgst_tax_rate": cgst_rate,
            "sgst_ledger": _id_name(),
            "sgst_tax_amount": sgst_amount,
            "sgst_tax_rate": sgst_rate,
            "rev_igst_ledger": _id_name(),
            "rev_igst_tax_amount": 0,
            "rev_cgst_ledger": _id_name(),
            "rev_cgst_tax_amount": 0,
            "rev_sgst_ledger": _id_name(),
            "rev_sgst_tax_amount": 0,
            "state_cess_rate": 0,
            "state_cess_amount": 0,
            "other_cess_rate": 0,
            "other_cess_amount": 0,
            "misc1_rate": 0, "misc1_value": 0,
            "misc2_rate": 0, "misc2_value": 0,
            "misc3_rate": 0, "misc3_value": 0,
            "document_misc1_value": 0,
            "document_misc2_value": 0,
            "document_misc3_value": 0,
            "document_overhead_value": 0,
            "effective_rate": self.rate,
            "advance_amount": 0,
            "attribute_list": [_id_name() for _ in range(5)],
            "service_date": "",
            "service_location": "",
            "posting_gl": _id_name(self.posting_gl_id, self.posting_gl_name),
            "parent": {"id": "", "ref_no": "", "ref_date": "", "vno": "", "vdate": ""},
            "remark": "",
            "warehouse": _id_name(self.warehouse_id, self.warehouse_name),
            "project": _id_name(),
            "work_order": _id_name(),
            "site": _id_name(),
            "project_activity": _id_name(),
            "barcode": "",
            "delivery_date": "",
            "mrp": 0,
            "net_price": 0,
            "salesman": _id_name(),
            "batch_detail": {"id": "", "batch_no": "", "mfg_date": "", "expiry_date": ""},
            "multi_details": [],
            "jobber_consumption_details": [],
            "barcode_details": [],
            "child_item_list": [],
            "dimension_details": [],
            "delivery_schedule": [],
            "promo_discount_qty": 0,
            "promo_discount_value": 0,
            "short_qty": 0,
            "rejection_qty": 0,
            "manual_taxable": False,
            "claimed_per": 0,
            "installation_required": 0,
            "promotion2_rate": 0,
            "promotion2_amount": 0,
            "coupon_discount_amount": 0,
        }


def build_document_shell(
    *,
    party_id: str,
    party_name: str = "",
    vdate: str = "",
    ref_no: str = "",
    ref_date: str = "",
    party_gst: str = "",
    billing_address: str = "",
    shipping_address: str = "",
    remark: str = "",
    location_id: str = "",
    location_name: str = "",
    category_id: str = "",
    category_name: str = "",
    currency_code: str = "INR",
    item_details: list[dict] | None = None,
) -> dict[str, Any]:
    """Build a base document/order/invoice structure.

    This provides the common shell used by SaveUpdate_Order, SaveUpdate_Invoice, etc.
    """
    return {
        "id": "",
        "common_property": {
            "edit_remark": "",
            "TransactionStatMode": 0,
            "readonly_reason": "",
            "approval_status": 0,
            "document_status": 0,
            "category_default_format": _id_name(),
            "vtime": "",
            "document_history_detail": None,
            "is_import_mode": None,
        },
        "location": _id_name(location_id, location_name),
        "category": _id_name(category_id, category_name),
        "party": _id_name(party_id, party_name),
        "location_state_id": "",
        "party_state_id": "",
        "party_email": "",
        "currency_code": currency_code,
        "conversion_rate": 1,
        "advance_amount": 0,
        "advance_gl": _id_name(),
        "tax_style": 0,
        "gst_type": 0,
        "salesman": _id_name(),
        "project": _id_name(),
        "tally_id": "",
        "voucher_number": {"prefix": "", "num": 0, "suffix": "", "vno": ""},
        "vdate": vdate,
        "ref_no": ref_no,
        "ref_date": ref_date or vdate,
        "work_order_description": "",
        "delivery_date": vdate,
        "agent": _id_name(),
        "billing_address": billing_address,
        "party_gst_no": party_gst,
        "party_contact_person": "",
        "shipping_address": shipping_address,
        "payment_term": _id_name(),
        "remark": remark,
        "document_billing_charges": {
            "misc1_rate": 0, "misc1_value": 0, "misc1_ledger": _id_name(),
            "misc2_rate": 0, "misc2_value": 0, "misc2_ledger": _id_name(),
            "misc3_rate": 0, "misc3_value": 0, "misc3_ledger": _id_name(),
            "overhead_per": 0, "overhead_value": 0, "overhead_ledger": _id_name(),
            "round_off_ledger": _id_name(),
            "round_off_value": 0,
            "tcs_rate": 0, "tcs_value": 0, "tcs_ledger": _id_name(),
        },
        "udf_list": ["", "", "", "", ""],
        "item_detail": item_details or [],
        "attachments": [],
        "shipping_address_master": _id_name(),
        "party_rate_info": {
            "party_id": party_id,
            "common_rate_per_unit": "",
            "last_rate": 0,
            "last_effective_rate": 0,
        },
        "document_extin": {
            "enable_logistic": False,
            "enable_payment_stage": False,
        },
        "place_of_supply": _id_name(),
        "logistic": {
            "transporter": _id_name(),
            "dispatch_from": "",
            "destination": "",
            "vehicle_no": "",
            "lr_no": "",
            "lr_date": "",
            "eway_bill_no": "",
            "eway_bill_date": "",
            "irn": "",
            "transport_mode": 0,
        },
        "payment_stage": _id_name(),
        "progress_milestone": _id_name(),
        "send_for_approval": False,
    }
