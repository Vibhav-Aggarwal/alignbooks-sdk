# AlignBooks Python SDK

Reverse-engineered Python client for AlignBooks ERP API.

## Installation

```bash
pip install git+https://github.com/Vibhav-Aggarwal/alignbooks-sdk.git
```

## Quick Start

```python
from alignbooks import AlignBooksClient

ab = AlignBooksClient(
    email="user@company.com",
    password="Password123",
    api_key="YOUR_API_KEY_UUID",
    enterprise_id="YOUR_ENTERPRISE_ID_UUID",
    company_id="YOUR_COMPANY_ID_UUID",
    user_id="YOUR_USER_ID_UUID"
)

# Get live stock
stock = ab.api_call("GetItemBalanceForList", {
    "voucher_type": 4,
    "branch_id": ab.ZERO_GUID,
    "warehouse_id": "YOUR_WAREHOUSE_ID_UUID"
})

# Direct SQL (MySQL)
items = ab.api_call("QueryExecute", {
    "query": "SELECT id, name FROM mst_item WHERE company_id='...' LIMIT 10"
})

# Send WhatsApp
ab.api_call("SendWhatsAppMessage", {
    "phone_nos": "919XXXXXXXXX",
    "message":   "Hello from AlignBooks",
    "attachments": []
})
```

## API Reference

See [docs/API_REFERENCE.md](docs/API_REFERENCE.md) for confirmed working endpoints.

## Discovery

**924 endpoints** extracted from AlignBooks web app `main.js`:
- 769 on `ABDataService.svc` (default)
- 32 on `ABUtilityService.svc` (SQL, WhatsApp, PDF)
- 58 on `ABConfigurationService.svc` (company setup)
- 31 on `ABReportService.svc` (GST, reports)
- 23 on `ABEnterpriseService.svc` (multi-company)
- 11 on `ABImportService.svc` (Excel, WhatsApp setup)

Full service map in `alignbooks/constants.py` → `SERVICE_MAP`.

## Key Endpoints

| Endpoint | What it does |
|----------|-------------|
| `QueryExecute` | Direct MySQL queries to ab007 DB |
| `GetItemBalanceForList` | Live stock levels |
| `List_Document` | Transaction lists (invoices, POs, etc.) |
| `ShortList_Customer` | Customer master |
| `ShortList_Vendor` | Vendor master |
| `SendWhatsAppMessage` | Send WhatsApp via configured API |
| `GetDocumentPrint` | Get document as PDF byte array |
| `SaveUpdate_Order` | Create Purchase Order |
| `SaveUpdate_Invoice` | Create Sales Invoice |

## Auth

All calls use `ab_token` header (AES-256-CBC encrypted JSON with credentials + timestamp).
Auto-handled by `AlignBooksClient.api_call()`.

See `alignbooks/auth.py` for encryption details.
