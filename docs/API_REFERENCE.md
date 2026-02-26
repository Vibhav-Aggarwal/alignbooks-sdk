# AlignBooks API Reference
> **Source:** Live testing on a production AlignBooks account + reverse-engineering AlignBooks `main.js` (24MB, 924 endpoints mapped)
> **Date:** 2026-02-26 | **Author:** AlignBooks SDK Contributors
> **Stats:** 19 endpoints tested · 14 confirmed working · 2 partial · 3 blocked

---

## TL;DR — The 3 Endpoints You Actually Need

```python
from alignbooks_client import api_call

# 1. Direct SQL — most powerful
rows = api_call("QueryExecute", {"query": "SELECT * FROM mst_item WHERE company_id='...' LIMIT 10"})

# 2. Live stock
stock = api_call("GetItemBalanceForList", {"voucher_type":4, "branch_id":ZERO, "warehouse_id":WAREHOUSE_GEN})

# 3. Any transaction list (invoices, orders, POs, payments...)
txns = api_call("List_Document", {"info":{"master_id":"","branch_id":ZERO,"from_date":"2025-04-01","to_date":"2026-02-28","master_type":4}})
```

---

## Authentication

Every call uses an `ab_token` header — AES-256-CBC encrypted JSON:

```python
header_info = {
    "username":      "email@example.com",
    "password":      "Password",
    "enterprise_id": "YOUR_ENTERPRISE_ID_UUID",
    "company_id":    "YOUR_COMPANY_ID_UUID",
    "user_id":       "YOUR_USER_ID_UUID",
    "apikey":        "YOUR_API_KEY_UUID",
    "master_type":   2037,
    "apiname":       "EndpointName",
    "client_date_time": "2026-02-26 15:00:00"
}
# Encrypt: AES-CBC, key=PBKDF2(b"YOUR_AES_KEY_32_BYTES_HERE", salt, 100 iters), IV=random16
# Token: base64(salt + iv + ciphertext)
```

**alignbooks_client.py** handles this automatically — just call `api_call(endpoint, body)`.

**Base URL:** `https://service.alignbooks.com`

---

## Service Map (924 endpoints)

| Service | URL | Count | Purpose |
|---------|-----|-------|---------|
| **ABDataService** | `/ABDataService.svc/{endpoint}` | **769** | Masters, transactions, stock, BOM, production — **default** |
| **ABUtilityService** | `/ABUtilityService.svc/{endpoint}` | 32 | SQL, WhatsApp, PDF, voucher numbers |
| **ABConfigurationService** | `/ABConfigurationService.svc/{endpoint}` | 58 | Company setup, permissions |
| **ABReportService** | `/ABReportService.svc/{endpoint}` | 31 | GST returns, custom reports |
| **ABImportService** | `/ABImportService.svc/{endpoint}` | 11 | Excel import, WhatsApp setup |
| **ABEnterpriseService** | `/ABEnterpriseService.svc/{endpoint}` | 23 | Multi-company, CRM |

Full 924-endpoint service map: `alignbooks/constants.py → SERVICE_MAP`

---

## ✅ Confirmed Working Endpoints

---

### `QueryExecute`
**Service:** ABUtilityService · **Type:** Direct SQL → MySQL ab007

```python
result = api_call("QueryExecute", {
    "query": "SELECT id, name, balance FROM et_stock_balance WHERE company_id='<company_id>' LIMIT 100"
})
# → list of dicts (raw MySQL rows)
```

**The most powerful endpoint.** Direct MySQL access to all 456 tables in the `ab007` database. No API abstraction — raw data.

**Rules:**
- MySQL syntax: `LIMIT` not `TOP`, backtick table names, no square brackets
- Always filter `WHERE company_id='<company_id>'` — DB is multi-tenant, all clients share it
- JOINs sometimes return "No Result" silently → split into 2 queries and merge in Python
- Use `information_schema.tables` to discover tables (`SHOW TABLES` returns empty)
- Responses with >5,000 rows may time out → use `LIMIT x OFFSET y` pagination

**Key tables in ab007 (456 total):**

| Table | Example Rows | Key Columns |
|-------|---------------|-------------|
| `mst_item` | 3,104 | id, name, code, group_id, sales_rate, purchase_rate, mrp |
| `mst_item_group` | 22 | id, name, code, parent_id |
| `mst_item_unit` | 48 | id, name, code |
| `mst_item_category` | 20 | id, name |
| `mst_party` | 547 | id, name, city, phone, gstin, party_type |
| `mst_ledger` | 336 | id, name, code, group_id, opening_balance |
| `mst_ledger_group` | 130 | id, name, parent_id |
| `mst_employee` | 15 | id, name, code |
| `mst_production_floor` | 4 | id, name, code |
| `mst_warehouse` | 18 | id, name, code |
| `et_stock_balance` | 33,975 | item_id, branch_id, warehouse_id, **balance** |
| `et_stock` | 315,232 | vtype, vno, vdate, item_id, qty, amount, party_id |
| `tr_bom` | 5,875 | finish_item_id, finish_qty, rm_item_id, rm_qty, sequence |
| `tr_bom_production` | 5,000+ | vno, vdate, finish_item_id, finish_qty |
| `tr_bom_production_detail` | 10,000+ | vid, item_id, qty, amount |
| `tr_production_floor_material` | 3,670 | vno, vdate, vtype(89), production_floor_id, finish_item_id |
| `tr_production_floor_material_detail` | 30,456 | vid, item_id, qty, amount |
| `con_setup_general` | 1 | whatsapp_url, whatsapp_user_name, email_from, email_smtp |
| `information_schema.tables` | 456 | table_name (WHERE table_schema='ab007') |

**Proven SQL queries:**

```sql
-- All tables in ab007
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'ab007' ORDER BY table_name

-- Live stock by item (with names)
SELECT i.name, SUM(sb.balance) as stock
FROM et_stock_balance sb
JOIN mst_item i ON i.id = sb.item_id
WHERE sb.company_id = '<company_id>'
GROUP BY i.id, i.name ORDER BY stock DESC

-- Today's cutting floor production (with item names - split query)
SELECT d.item_id, d.qty FROM tr_production_floor_material p
JOIN tr_production_floor_material_detail d ON d.vid = p.id
WHERE p.company_id = '<company_id>' AND p.vdate = '2026-02-26'

-- BOM for a finished product
SELECT ri.name as raw_material, b.rm_qty, b.finish_qty
FROM tr_bom b JOIN mst_item ri ON ri.id = b.rm_item_id
WHERE b.company_id = '<company_id>' AND b.finish_item_id = '<item_uuid>'

-- WhatsApp + SMTP config
SELECT whatsapp_url, whatsapp_user_name, whatsapp_password,
       email_from, email_smtp, email_port
FROM con_setup_general WHERE company_id = '<company_id>'
```

---

### `GetItemBalanceForList`
**Service:** ABDataService · **Type:** Live stock levels

```python
result = api_call("GetItemBalanceForList", {
    "voucher_type": 4,
    "branch_id":    "00000000-0000-0000-0000-000000000000",  # all branches
    "warehouse_id": "YOUR_WAREHOUSE_ID_UUID"  # "general" warehouse
})
# → [{"item_id": "uuid", "balance": 690.0}, ...]
# Example: 1,952 items returned
```

**Notes:**
- `warehouse_id` must be a real warehouse UUID — zero GUID returns empty
- Cross-reference `item_id` with `mst_item.id` for names (or use QueryExecute JOIN)
- Negative balance = production issued more than received (40 items in example)
- Faster than QueryExecute for current stock snapshot

---

### `List_Document`
**Service:** ABDataService · **Type:** Transaction headers list

```python
result = api_call("List_Document", {
    "info": {
        "master_id":   "",
        "branch_id":   "00000000-0000-0000-0000-000000000000",
        "from_date":   "2025-04-01",
        "to_date":     "2026-02-28",
        "master_type": 4   # ← VType number
    }
})
# → list of transaction header dicts
```

**VType reference:**

| VType | Name | Example Count |
|-------|------|--------------|
| 3 | Sales Order | 3,514 |
| 4 | Sales Invoice | 3,460 |
| 5 | Dispatch (Delivery Challan) | 41 |
| 6 | Sales Return / Credit Note | 4 |
| 7 | Customer Receipt (Payment) | 3,137 |
| 16 | Purchase Order | 394 |
| 18 | Purchase Bill | 1,883 |
| 19 | Purchase Return / Debit Note | 10 |
| 22 | Vendor Payment | 1,581 |
| 80 | Jobcard (Production) | 1 |
| 87 | Issue Request from Floor | — |
| 88 | Material Issue to Floor | — |
| 89 | Material Received from Floor ← **daily cutting records** | 3,670 |

**Notes:**
- Returns headers only — no line items. Use `Display_Invoice` for detail
- Server may ignore date filters — filter client-side after fetching
- `branch_id` zero GUID = all branches

---

### `ShortList_Customer` / `ShortList_Vendor`
**Service:** ABDataService

```python
customers = api_call("ShortList_Customer", {"new_id": "00000000-0000-0000-0000-000000000000"})
vendors   = api_call("ShortList_Vendor",   {"new_id": "00000000-0000-0000-0000-000000000000"})
# → [{id, name, city, phone, gstin, credit_limit, credit_days, ...}]
# Example: 225 customers, 351 vendors
```

---

### `Display_Invoice`
**Service:** ABDataService · ⚠️ Purchase bills only

```python
# ✅ Works for Purchase Bills (VType 18)
invoice = api_call("Display_Invoice", {"id": "<uuid>", "vtype": 18})

# ❌ FAILS for Sales Invoices (VType 4) — "No rights"
```

Returns full invoice object including item lines, tax breakdown, party details.
Use to clone structure when creating new bills (`SaveUpdate_Invoice`).

---

### `GetItemAnalysis`
**Service:** ABDataService

```python
result = api_call("GetItemAnalysis", {
    "item_id": "<item_uuid>",
    "vdate":   "2026-02-26"
})
# → sales/purchase movement analysis for the item as of vdate
```

---

### `GetMovedOnlyStock`
**Service:** ABDataService

```python
result = api_call("GetMovedOnlyStock", {
    "from_date": "2026-02-01",
    "to_date":   "2026-02-26"
})
# → items with stock movement (bought/sold/transferred) in period
```

---

### `GetLogisticBulkUpdateData`
**Service:** ABDataService · **Type:** Courier/shipping tracker

```python
result = api_call("GetLogisticBulkUpdateData", {
    "VType":     5,
    "from_date": "2026-01-01",
    "to_date":   "2026-02-26"
})
# → dispatches with courier name, AWB number, tracking status
```

---

### `SendWhatsAppMessage`
**Service:** ABUtilityService

```python
result = api_call("SendWhatsAppMessage", {
    "phone_nos":   "91XXXXXXXXXX",  # without + prefix
    "message":     "Message text",
    "attachments": []
})
# → {"ReturnCode": 0, ...}
```

Requires `whatsapp_url` in `con_setup_general`. Proxies to messageautosender.com.
**Direct API is faster** — see below.

---

### `GetDocumentPrint`
**Service:** ABUtilityService · **Type:** PDF generation

```python
result = api_call("GetDocumentPrint", {
    "voucher_id":                 "<invoice_uuid>",
    "vtype":                      18,
    "format_id":                  "33d35889-1871-11ed-a132-005056a578c5",
    "digital_signature_selected": False,
    "copies":                     1
})
pdf_bytes = bytes(result["DocumentFile"])  # list of ints → bytes
```

---

### `SaveUpdate_Order` — Create Purchase Order
**Service:** ABDataService · VType 16

```python
result = api_call("SaveUpdate_Order", {
    "is_new_mode": True,
    "vtype":       16,
    "info": {
        "id":    "00000000-0000-0000-0000-000000000000",
        "vtype": 16,
        "party": {"id": "<vendor_uuid>"},
        "vdate": "2026-02-26 00:00:00",
        "voucher_number": {"digits":0, "num":0, "prefix":"GG", "suffix":"", "vno":""},
        "currency": "INR",
        "send_for_approval":        False,  # ← MUST be False, not None
        "is_import_mode":           False,  # ← MUST be False, not None
        "document_history_detail":  [],     # ← MUST be [], not None
        "udf_list":                 [],
        "document_extin": {"brand": "", "procurement_type": "", "rate_category": ""},
        "tax_style": 1,
        "item_list": [{
            "item": {"id": "<item_uuid>"},
            "unit": {"id": "<unit_uuid>"},
            "qty":    100,
            "rate":   50.0,
            "amount": 5000.0
        }]
    }
})
```

**Critical gotchas:**
- `send_for_approval: None` → C# NullReferenceException crash
- `document_history_detail: None` → crash
- `voucher_number.suffix: None` → crash
- VType **16** for PO (not 14!)
- Working template: `create_kc_po.py`

---

### `SaveUpdate_Invoice` — Create Purchase Bill
**Service:** ABDataService · VType 18

```python
result = api_call("SaveUpdate_Invoice", {
    "is_new_mode": True,
    "vtype":       18,
    "invoice":     { ... }  # ← key is "invoice" not "info"!
})
```

Clone structure from `Display_Invoice` of an existing bill, change IDs to zero GUID.
Working template: `create_purchase_bill.py`

---

### `Display_ProductionFloorMaterial`
**Service:** ABDataService

```python
result = api_call("Display_ProductionFloorMaterial", {
    "id":    "<production_entry_uuid>",
    "vtype": 89
})
# → full production entry with all material line items
```

---

## 🌐 Direct WhatsApp API (Not AlignBooks)

AlignBooks proxies to messageautosender.com — call it directly for speed:

```python
import requests

r = requests.post(
    "https://app.messageautosender.com/api/v1/message/create",
    json={
        "username": "YOUR_WHATSAPP_USERNAME",
        "password": "YOUR_WHATSAPP_PASSWORD",
        "to":       "919XXXXXXXXX",  # 91 + number, no +
        "body":     "Message text"
    },
    timeout=15
)
# → {"status": 200, "message": "success", "result": {"id": ...}}
```

**Helper:** `send_whatsapp(phone, message)` in `alignbooks_client.py`

---

## ❌ Blocked Endpoints

| Endpoint | Error | Workaround |
|----------|-------|-----------|
| `Display_Invoice` VType 4 | RC 5000 "No rights" | `QueryExecute` on `et_stock WHERE vtype=4` |
| `GetReportFilter` | RC 5002 Invalid Input | `QueryExecute` direct SQL |
| `GetStockStatementForBank` | Returns PDF, not JSON | `QueryExecute` on `et_stock_balance` |

---

## Your Company Constants

```python
COMPANY_ID    = "YOUR_COMPANY_ID_UUID"
ENTERPRISE_ID = "YOUR_ENTERPRISE_ID_UUID"
USER_ID       = "YOUR_USER_ID_UUID"
ZERO_GUID     = "00000000-0000-0000-0000-000000000000"
BRANCH_MAIN   = "YOUR_BRANCH_ID_UUID"
WAREHOUSE_GEN = "YOUR_WAREHOUSE_ID_UUID"  # "general"

# Production floors
FLOOR_CUTTING   = "YOUR_CUTTING_FLOOR_ID_UUID"  # daily 0001
FLOOR_PACKAGING = "YOUR_PACKAGING_FLOOR_ID_UUID"  # 0002
FLOOR_PAD_PRINT = "YOUR_PAD_PRINT_FLOOR_ID_UUID"  # 0003
FLOOR_SCREENING = "YOUR_SCREENING_FLOOR_ID_UUID"  # 0004
```

---

## Quick Reference: VType Numbers

```python
# Sales
SALES_ORDER   = 3;  SALES_INVOICE  = 4;  DISPATCH    = 5
SALES_RETURN  = 6;  CUST_RECEIPT   = 7;  ESTIMATE    = 2

# Purchase
PURCHASE_ORDER = 16; PURCHASE_BILL = 18; PURCH_RETURN = 19
VENDOR_PAYMENT = 22; GRN           = 20

# Production
JOBCARD            = 80
ISSUE_TO_FLOOR     = 87
ISSUE_TO_FLOOR_2   = 88
RECEIVED_FROM_FLOOR= 89   # ← Daily cutting floor records
```

---

## ab007 Database Tables (456 total)

Discovered via `QueryExecute` on `information_schema.tables`.
Pulled into `alignbooks_mirror.db` (SQLite exact mirror).

**Table prefix guide:**

| Prefix | Count | Contents |
|--------|-------|----------|
| `tr_` | 127 | Transactions (invoices, orders, payments, BOM, production) |
| `mst_` | 118 | Masters (items, parties, ledgers, employees) |
| `con_` | 61 | Configuration (setup, permissions, numbering) |
| `abcrm_` | 20 | CRM (contacts, prospects, actions) |
| `log_` | 24 | Audit logs |
| `et_` | 28 | Enterprise/stock (et_stock, et_stock_balance — key tables) |
| `ab_` | 9 | Global lookups (countries, currencies) |

**Highest-value tables:**

| Table | Example Rows | Notes |
|-------|-------------|-------|
| `et_stock` | **315,232** | Every stock movement since day 1 |
| `et_stock_balance` | 33,975 | Current balance per item+branch+warehouse |
| `tr_bom` | 5,875 | Bill of Materials |
| `tr_production_floor_material_detail` | 30,456 | Daily production line items |
| `tr_production_floor_material` | 3,670 | Daily production entries |
| `mst_item` | 3,104 | Item master |
| `mst_party` | 547 | All customers + vendors combined |

---

## Files in This Repo

| File | Contents |
|------|----------|
| `alignbooks/constants.py` | SERVICE_MAP (924 endpoints), VType enum, Company IDs |
| `alignbooks/client.py` | `AlignBooksClient` — handles auth, retries, service routing |
| `docs/API_REFERENCE.md` | This file |
| `endpoint_status.json` | Test results: 19 tested, 14 working, 2 partial, 3 blocked |

---

*Last updated: 2026-02-26 · Reverse-engineered from AlignBooks main.js (24MB) + live testing*
