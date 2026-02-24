"""Constants for AlignBooks SDK."""

# Zero GUID used for new records
ZERO_GUID = "00000000-0000-0000-0000-000000000000"

# API Base URL
API_BASE = "https://service.alignbooks.com"

# AES encryption key (32 bytes UTF-8)
AES_KEY = b"01432587690321654987210543876901"

# AES IV for login response decryption (16 zero bytes)
AES_IV_ZERO = b"\x00" * 16

# PBKDF2 iterations for ab_token generation
PBKDF2_ITERATIONS = 100
PBKDF2_KEY_LENGTH = 32

# Default master_type for auth
DEFAULT_MASTER_TYPE = 2037


class Service:
    """Service URL suffixes."""
    DATA = "ABDataService.svc"
    UTILITY = "ABUtilityService.svc"
    CONFIG = "ABConfigurationService.svc"
    REPORT = "ABReportService.svc"
    IMPORT = "ABImportService.svc"
    ENTERPRISE = "ABEnterpriseService.svc"


# Endpoint → Service mapping for non-default services
# Default is ABDataService
SERVICE_MAP: dict[str, str] = {
    # Utility
    "GetDocumentPrint": Service.UTILITY,
    "GetDocumentURLInfo": Service.UTILITY,
    "GetPrintFormatList": Service.UTILITY,  # Note: also exists on DataService
    "GetCompleteCurrencyList": Service.UTILITY,
    "GetCompanySelectionList": Service.UTILITY,
    "GetFinancialPeriodList": Service.UTILITY,
    "GetVoucherNumber": Service.UTILITY,
    "GetMasterCode": Service.UTILITY,
    "GetLinkageParent": Service.UTILITY,
    "GetSampleDocumentPreview": Service.UTILITY,
    "GetVideoLink": Service.UTILITY,
    "GetDataForQuery": Service.UTILITY,
    "GetFilterForQuery": Service.UTILITY,
    "ChangePassword": Service.UTILITY,
    "ValidatePasswordPolicy": Service.UTILITY,
    "SendVoucherEmail": Service.UTILITY,
    "SendVoucherSMS": Service.UTILITY,
    "SendVoucherMailLink": Service.UTILITY,
    "SendWhatsAppMessage": Service.UTILITY,
    "SendReport": Service.UTILITY,
    "SendForgotPasswordOTP": Service.UTILITY,
    "ResetCompanyStatic": Service.UTILITY,
    "UpdateDefaultCompany": Service.UTILITY,
    "UpdateCustomerRemark": Service.UTILITY,
    "QueryExecute": Service.UTILITY,
    "SaveFavouriteMenu": Service.UTILITY,
    "DeleteFavouriteMenu": Service.UTILITY,
    "GetFavouriteMenu": Service.UTILITY,
    "ContactManagementSendEmailSMS": Service.UTILITY,
    "PickPackSendEmailSMS": Service.UTILITY,
    "ResendCommunication": Service.UTILITY,
    "ICICINewAccountRequest": Service.UTILITY,
    "TextToSpeech": Service.UTILITY,
    # Configuration
    "Display_CompanySetup": Service.CONFIG,
    "Display_CompanyImage": Service.CONFIG,
    "Display_DashboardConfiguration": Service.CONFIG,
    "Display_DocumentGeneralSetup": Service.CONFIG,
    "Display_DocumentNumberingSetup": Service.CONFIG,
    "Display_DocumentApprovalSetup": Service.CONFIG,
    "Display_EmailSMSSetup": Service.CONFIG,
    "Display_PrintConfiguration": Service.CONFIG,
    "Display_UserPermission": Service.CONFIG,
    "Display_DigitalSignatureSetup": Service.CONFIG,
    "Display_ScheduleConfiguration": Service.CONFIG,
    "Display_Integration_Config": Service.CONFIG,
    "Display_MasterApprovalConfiguration": Service.CONFIG,
    "Display_HROtherSetup": Service.CONFIG,
    "Display_HROvertimeSetup": Service.CONFIG,
    "Display_HRPerquisiteSetup": Service.CONFIG,
    "Display_HRSalarySetup": Service.CONFIG,
    "Display_HRStatutorySetup": Service.CONFIG,
    "Display_GhanaTaxcodeMapping": Service.CONFIG,
    "DisplayAuthoriseCompanyToPullData": Service.CONFIG,
    "DisplayUserMenuRights": Service.CONFIG,
    "GetCompaniesListofEnterprise": Service.CONFIG,
    "GetDashboardConfig": Service.CONFIG,
    "GetObjectRights": Service.CONFIG,
    "GetPasswordPolicy": Service.CONFIG,
    "SaveUpdate_DashboardConfiguration": Service.CONFIG,
    "SaveUpdate_DocumentGeneralSetup": Service.CONFIG,
    "SaveUpdate_DocumentNumberingSetup": Service.CONFIG,
    "SaveUpdate_PrintConfiguration": Service.CONFIG,
    "SaveUpdate_UserPermission": Service.CONFIG,
    "SaveUpdate_DigitalSignatureSetup": Service.CONFIG,
    "SaveUpdate_ScheduleConfiguration": Service.CONFIG,
    "SaveUpdate_Integration_Config": Service.CONFIG,
    "SaveUpdate_HROtherSetup": Service.CONFIG,
    "SaveUpdate_HROvertimeSetup": Service.CONFIG,
    "SaveUpdate_HRPerquisiteSetup": Service.CONFIG,
    "SaveUpdate_HRSalarySetup": Service.CONFIG,
    "SaveUpdate_HRStatutorySetup": Service.CONFIG,
    "SaveDocumentApprovalConfiguration": Service.CONFIG,
    "SaveEmail_SMSConfiguration": Service.CONFIG,
    "SaveUserMenuRights": Service.CONFIG,
    "SaveAuthoriseCompanyToPullData": Service.CONFIG,
    "SaveChildCompanyVsCustomerMapping": Service.CONFIG,
    "SaveUnmappedItemAccrossCompany": Service.CONFIG,
    "Save_ApprovalAdvancement": Service.CONFIG,
    "Save_GhanaTaxcodeMapping": Service.CONFIG,
    "Save_MasterApprovalConfiguration": Service.CONFIG,
    "DeleteUserMenuRights": Service.CONFIG,
    "CopyCompanyData": Service.CONFIG,
    "Update_CompanyBasicSetup": Service.CONFIG,
    "Update_CompanyFinanceSetup": Service.CONFIG,
    "Update_CompanyGeneralSetup": Service.CONFIG,
    "Update_CompanyGeneralSetup_LockUpto": Service.CONFIG,
    "Update_CompanyInventorySetup": Service.CONFIG,
    "Update_CompanyPurchaseSetup": Service.CONFIG,
    "Update_CompanySalesSetup": Service.CONFIG,
    "Update_DefaultGL": Service.CONFIG,
    "Update_Integration_ConfigStatus": Service.CONFIG,
    # Report
    "GetReportData": Service.REPORT,
    "GetReportFilter": Service.REPORT,
    "GetReportView": Service.REPORT,
    "GetReportPrintPDF": Service.REPORT,
    "GetReportPrintExportDetailToExcel": Service.REPORT,
    "GetReportPrintExportDetailToNotepad": Service.REPORT,
    "GetUserReportColumn": Service.REPORT,
    "GetCalculativeColumns": Service.REPORT,
    "GetFavouriteReportMenu": Service.REPORT,
    "GetGSTR1Json": Service.REPORT,
    "GetGSTR3B": Service.REPORT,
    "GetGSTR3BJson": Service.REPORT,
    "GetGSTR4Json": Service.REPORT,
    "GetGSTR9Json": Service.REPORT,
    "GetVATReturn_MiddleEastJson": Service.REPORT,
    "GetStockStatementForBank": Service.REPORT,
    "GetVoucerListForFilter": Service.REPORT,
    "DisplayCustomReport": Service.REPORT,
    "ListReportView": Service.REPORT,
    "SaveCustomReport": Service.REPORT,
    "SaveReportInFavourite": Service.REPORT,
    "SaveUserReportColumn": Service.REPORT,
    "SaveUserReportCalculativeColumn": Service.REPORT,
    "SetAsDefaultView": Service.REPORT,
    "DeleteReportFromFavourite": Service.REPORT,
    "DeleteView": Service.REPORT,
    "DownloadEInvoiceJson": Service.REPORT,
    "DownloadEWayBillJson": Service.REPORT,
    "DownloadFTAVATAuditFile": Service.REPORT,
    "GenerateLoanAccountConfirmation": Service.REPORT,
    "GenerateOTPGSTR1": Service.REPORT,
    "GeneratePartyAccountConfirmation": Service.REPORT,
    "GeneratePaySlip": Service.REPORT,
    "GeneratePaymentReminder": Service.REPORT,
    "UploadGSTR1": Service.REPORT,
    # Import
    "SaveExternal_Invoice": Service.IMPORT,
    "Import_Master": Service.IMPORT,
    "ImportFromSAP": Service.IMPORT,
    "ExportVoucherToExcel": Service.IMPORT,
    "Display_ExcelColumnMapping": Service.IMPORT,
    "Save_ExcelColumnMapping": Service.IMPORT,
    "Delete_ExcelColumnMapping": Service.IMPORT,
    "GetIPAddress": Service.IMPORT,
    "WhatsAppWeb_Register": Service.IMPORT,
    "WhatsAppWeb_StatusChecking": Service.IMPORT,
    "WhatsAppWeb_MobileLinkage": Service.IMPORT,
    "WhatsAppWeb_PurchasePlan": Service.IMPORT,
    # Enterprise
    "CreateCompany": Service.ENTERPRISE,
    "DeleteCompany": Service.ENTERPRISE,
    "CreateGuestUser": Service.ENTERPRISE,
    "GetClientListForUser": Service.ENTERPRISE,
    "GetLicenseInfoForEnterprise": Service.ENTERPRISE,
    "GetSubscriptionInfo": Service.ENTERPRISE,
    "GetCRMReport": Service.ENTERPRISE,
    "SaveLicenseOrder": Service.ENTERPRISE,
    "UpdateUserProfile": Service.ENTERPRISE,
    "UpdateEnterpriseOffer": Service.ENTERPRISE,
    "UpdateLicenseOrderStatus": Service.ENTERPRISE,
    "ValidateGuestUserInCompany": Service.ENTERPRISE,
    "ValidateURL": Service.ENTERPRISE,
    "VerifyUniqueUser": Service.ENTERPRISE,
    "ProcessURL": Service.ENTERPRISE,
    "ListSalesPartner": Service.ENTERPRISE,
    "IVR_ClickToCall": Service.ENTERPRISE,
    "ABCRM_IVR_ClickToCall": Service.ENTERPRISE,
    "CRMTrn_GetTopicForTrainingFeedback": Service.ENTERPRISE,
    "CRMTrn_SaveTrainingFeedback": Service.ENTERPRISE,
    "InAppFeedbackFromMobile": Service.ENTERPRISE,
    "Save_Survey": Service.ENTERPRISE,
    "support_SaveSupportTicket": Service.ENTERPRISE,
}


class VType:
    """Document/voucher type codes (from AbMenuMaster enum in main.js)."""
    SALES_ESTIMATE = 1
    SALES_ORDER = 3
    SALES_INVOICE = 4
    DISPATCH = 5
    SALES_RETURN = 6
    DELIVERY_CHALLAN = 7
    PURCHASE_ORDER = 16
    PURCHASE_BILL = 18
    GOODS_RECEIPT_NOTE = 20
    PURCHASE_RETURN = 21
    PURCHASE_CHALLAN = 22
    PAYMENT_VOUCHER = 8
    RECEIPT_VOUCHER = 9
    JOURNAL_VOUCHER = 10
    CONTRA_VOUCHER = 11
    CREDIT_NOTE = 12
    DEBIT_NOTE = 13
    STOCK_TRANSFER = 23
    STOCK_ADJUSTMENT = 24
    MATERIAL_ADJUSTMENT = 25
    PRODUCTION = 26
    EXPENSE_JOURNAL = 27
    PURCHASE_REQUISITION = 30


class MasterType:
    """Master type codes for ShortList calls."""
    CUSTOMER = 1
    VENDOR = 2
    ITEM = 3
    LEDGER = 4
    ITEM_GROUP = 5
    ITEM_CATEGORY = 6
    ITEM_UNIT = 7
    PARTY_CATEGORY = 8
    LOCATION = 9
    WAREHOUSE = 10
    CURRENCY = 11
    TAX_CODE = 12
    BRAND = 14
    AGENT = 15
    SALES_EXECUTIVE = 16
    TERRITORY = 17
    PAYMENT_TERMS = 18
    STATE = 19
    COUNTRY = 20
    CITY = 21
    TRANSPORTER = 22
    DOCUMENT_CATEGORY = 23
    EMPLOYEE = 24
    USER = 2037


# Body key mapping for SaveUpdate endpoints
# CRITICAL: Using wrong key causes "Object reference not set" errors
SAVE_BODY_KEY: dict[str, str] = {
    "SaveUpdate_Invoice": "invoice",
    "SaveUpdate_Order": "info",
    "SaveUpdate_Item": "item_information",
    "SaveUpdate_Party": "info",
    "SaveUpdate_Ledger": "info",
    "SaveUpdate_JournalVoucher": "info",
    "SaveUpdate_PaymentReceiptVoucher": "info",
    "SaveUpdate_Estimate": "info",
    "SaveUpdate_Challan": "info",
    "SaveUpdate_MaterialAdjustment": "info",
    "SaveUpdate_Jobwork": "info",
    "SaveUpdate_InterBranch": "info",
    "SaveUpdate_BOMBasedProduction": "info",
    "SaveUpdate_ExpenseJournalVoucher": "info",
    "SaveUpdate_PurchaseRequisition": "info",
}


# Indian states with GST state codes
INDIAN_STATES: dict[str, str] = {
    "01": "Jammu & Kashmir",
    "02": "Himachal Pradesh",
    "03": "Punjab",
    "04": "Chandigarh",
    "05": "Uttarakhand",
    "06": "Haryana",
    "07": "Delhi",
    "08": "Rajasthan",
    "09": "Uttar Pradesh",
    "10": "Bihar",
    "11": "Sikkim",
    "12": "Arunachal Pradesh",
    "13": "Nagaland",
    "14": "Manipur",
    "15": "Mizoram",
    "16": "Tripura",
    "17": "Meghalaya",
    "18": "Assam",
    "19": "West Bengal",
    "20": "Jharkhand",
    "21": "Odisha",
    "22": "Chhattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "26": "Dadra & Nagar Haveli and Daman & Diu",
    "27": "Maharashtra",
    "28": "Andhra Pradesh (Old)",
    "29": "Karnataka",
    "30": "Goa",
    "31": "Lakshadweep",
    "32": "Kerala",
    "33": "Tamil Nadu",
    "34": "Puducherry",
    "35": "Andaman & Nicobar Islands",
    "36": "Telangana",
    "37": "Andhra Pradesh",
    "38": "Ladakh",
}
