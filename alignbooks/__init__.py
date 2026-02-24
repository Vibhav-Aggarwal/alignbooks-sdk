"""AlignBooks Python SDK.

An unofficial, reverse-engineered API client for AlignBooks Accounting & ERP.
"""

from .client import AlignBooksClient
from .services import (
    ConfigService,
    CustomersService,
    DocumentsService,
    FinanceService,
    InventoryService,
    ItemsService,
    LedgersService,
    MastersService,
    PurchaseService,
    ReportsService,
    SalesService,
    VendorsService,
)

__version__ = "0.1.0"


class AlignBooks(AlignBooksClient):
    """Main facade for the AlignBooks SDK.

    This class extends the core client and attaches all service modules
    as properties for easy, discoverable access to the API.

    Example:
        >>> from alignbooks import AlignBooks
        >>> ab = AlignBooks(email="...", password="...", api_key="...", ...)
        >>> vendors = ab.vendors.list()
        >>> pdf_bytes, name = ab.documents.get_pdf(doc_id, vtype=18)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.masters = MastersService(self)
        self.vendors = VendorsService(self)
        self.customers = CustomersService(self)
        self.items = ItemsService(self)
        self.ledgers = LedgersService(self)
        
        self.purchase = PurchaseService(self)
        self.sales = SalesService(self)
        self.finance = FinanceService(self)
        self.inventory = InventoryService(self)
        self.reports = ReportsService(self)
        self.config = ConfigService(self)
        self.documents = DocumentsService(self)

__all__ = ["AlignBooks", "AlignBooksClient"]
