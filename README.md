# AlignBooks Python SDK

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An **unofficial, reverse-engineered** Python SDK for the [AlignBooks](https://alignbooks.com/) Accounting and ERP API. 

AlignBooks does not provide an official public SDK. This library wraps their internal WCF services, handling AES encryption, `ab_token` generation, session management, and endpoint mappings to give you a clean, Pythonic interface.

## Disclaimer
> **This is an unofficial project.** We are not affiliated with, endorsed by, or sponsored by Align Info Solutions Pvt. Ltd. This SDK relies on reverse-engineered API endpoints which may change without notice. Use in production at your own risk.

## Installation

```bash
pip install alignbooks-sdk
```

*(Note: Currently, you may need to install from source or GitHub until published to PyPI)*
```bash
pip install git+https://github.com/genautollp/alignbooks-sdk.git
```

## Quick Start

You'll need your AlignBooks credentials, including the hidden `api_key`, `enterprise_id`, `company_id`, and `user_id`. (These can be extracted by inspecting the network traffic in the AlignBooks web app).

```python
from alignbooks import AlignBooks

ab = AlignBooks(
    email="user@example.com",
    password="your-password",
    api_key="your-api-key",
    enterprise_id="your-enterprise-id",
    company_id="your-company-id",
    user_id="your-user-id"
)

# Auto-login happens on the first call
vendors = ab.vendors.list()
for vendor in vendors:
    print(f"Vendor: {vendor['name']} (ID: {vendor['id']})")
```

## API Reference

The SDK is organized into service modules accessible as properties on the main client.

### Masters (Vendors, Customers, Items, Ledgers)

```python
# List items
items = ab.items.list()

# Get a specific customer
customer = ab.customers.get("customer-guid")

# Create a new vendor
new_vendor = ab.vendors.create({
    "name": "Test Vendor",
    "gst_no": "06XXXXX...",
    "state": {"id": "state-guid"}
})
```

### Documents (Invoices, Bills, Orders)

```python
from alignbooks.constants import VType

# List Purchase Bills
bills = ab.purchase.list_bills(from_date="2026-01-01", to_date="2026-02-24")

# Delete a document
ab.documents.delete("document-guid", vtype=VType.PURCHASE_BILL)

# Download PDF
pdf_bytes, filename = ab.documents.get_pdf("document-guid", vtype=VType.PURCHASE_BILL)
with open(filename, "wb") as f:
    f.write(pdf_bytes)
```

## Examples

Check the `examples/` directory in this repository for full scripts, including:
- Creating a Purchase Order
- Creating a Purchase Bill with taxes
- Generating PDFs
- Managing Authentication

## Configuration via Environment Variables

It's highly recommended to use environment variables for your credentials. You can use a `.env` file:

```env
AB_EMAIL=user@example.com
AB_PASSWORD=your-password
AB_API_KEY=09b71bca-...
AB_ENTERPRISE_ID=73c22444-...
AB_COMPANY_ID=7e945776-...
AB_USER_ID=0b74dd56-...
```

## Reverse Engineering Notes
- AlignBooks uses PBKDF2 with an AES-256-CBC cipher to encrypt an auth payload containing your session and API keys into an `ab_token` header.
- Endpoint naming generally follows `SaveUpdate_MasterName` and `ShortList_MasterName`.
- When creating transactions, note the JSON key required varies by VType (e.g. `SaveUpdate_Invoice` requires `"invoice"`, `SaveUpdate_Order` requires `"info"`).

## License

MIT License. See [LICENSE](LICENSE) for more information.
