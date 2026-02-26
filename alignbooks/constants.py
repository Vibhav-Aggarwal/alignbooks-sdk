"""
AlignBooks SDK Constants
Full service mapping extracted from AlignBooks web app main.js (2026-02-26)
924 endpoints discovered. Default service: ABDataService.svc (769 endpoints)
Non-default service endpoints (155) are mapped explicitly below.
"""

# Zero GUID used for new records / "all" filters
ZERO_GUID = "00000000-0000-0000-0000-000000000000"

# API Base URL
API_BASE = "https://service.alignbooks.com"

# AES encryption key (32 bytes UTF-8)
AES_KEY = b"YOUR_AES_KEY_32_BYTES_HERE"

# AES IV for login response decryption (16 zero bytes)
AES_IV_ZERO = b"\x00" * 16

# PBKDF2 iterations for ab_token generation
PBKDF2_ITERATIONS = 100
PBKDF2_KEY_LENGTH = 32

# Default master_type for auth
DEFAULT_MASTER_TYPE = 2037


class Service:
    """Service URL suffixes (append to https://service.alignbooks.com/)"""
    DATA          = "ABDataService.svc"          # Default — 769 endpoints
    UTILITY       = "ABUtilityService.svc"        # 32 endpoints (reports, WA, SQL)
    CONFIG        = "ABConfigurationService.svc"  # 58 endpoints (company setup)
    REPORT        = "ABReportService.svc"         # 31 endpoints (PDF reports, GST)
    IMPORT        = "ABImportService.svc"         # 11 endpoints (Excel, WhatsApp setup)
    ENTERPRISE    = "ABEnterpriseService.svc"     # 23 endpoints (multi-company)


class VType:
    """
    AlignBooks Voucher Types (Et_* enum from ABMenuMaster).
    Pass as master_type in List_Document, Display_Invoice, etc.
    """
    # ── Sales ─────────────────────────────────────────────────
    SALES_ORDER            = 3    # Et_SalesOrder
    SALES_INVOICE          = 4    # Et_SalesInvoice
    DISPATCH               = 5    # Et_Dispatch (Delivery Challan)
    SALES_RETURN           = 6    # Et_SalesReturn (Credit Note)
    SALES_CHALLAN          = 7    # Et_SalesChallan (used as Payment Receipt in example)
    ESTIMATE               = 2    # Et_Estimate
    PURCHASE_REQUISITION   = 60   # Et_PurchaseRequisition

    # ── Purchase ──────────────────────────────────────────────
    PURCHASE_ORDER         = 16   # Et_PurchaseOrder
    PURCHASE_BILL          = 18   # Et_PurchaseBill
    PURCHASE_RETURN        = 19   # Et_PurchaseReturn (Debit Note)
    GOODS_RECEIPT_NOTE     = 20   # Et_GoodsReceiptNote
    PURCHASE_CHALLAN       = 22   # Et_PurchaseChallan (Vendor Payment in example)

    # ── Inventory / Stock Transfer ─────────────────────────────
    MATERIAL_ADJUSTMENT    = 35   # Et_MaterialAdjustment
    INTER_BRANCH           = 38   # Et_InterBranch (Stock Transfer)
    JOBWORK_OUTWARD        = 48   # Et_JobWorkOutwardInvoice
    JOBWORK_INWARD         = 79   # Et_JobWorkInwardInvoice

    # ── Production ────────────────────────────────────────────
    JOBCARD                = 80   # Et_Jobcard
    MAT_ISSUE_JOBCARD      = 81   # Et_MaterialIssueAgainstJobcard
    MAT_RECEIVED_JOBCARD   = 82   # Et_MaterialReceivedAgainstJobcard
    CLOSE_JOBCARD          = 84   # Et_CloseJobcard
    MAT_ISSUE_FLOOR        = 87   # Et_IssueRequestFromProductionFloor
    MAT_ISSUE_FLOOR2       = 88   # Et_MaterialIssueToProductionFloor
    MAT_RECEIVED_FLOOR     = 89   # Et_MaterialReceivedFromProductionFloor (daily cuts )

    # ── Finance ───────────────────────────────────────────────
    PAYMENT_RECEIPT        = 9    # Et_PaymentReceipt
    JOURNAL                = 10   # Et_JournalVoucher
    CREDIT_NOTE            = 14   # Et_CreditNote
    DEBIT_NOTE             = 15   # Et_DebitNote


# Company credentials removed — use environment variables or .env file
SERVICE_MAP: dict[str, str] = {
    # ── ABConfigurationService.svc (58 endpoints)
    "CopyCompanyData": Service.CONFIG,
    "DeleteUserMenuRights": Service.CONFIG,
    "DisplayAuthoriseCompanyToPullData": Service.CONFIG,
    "DisplayUserMenuRights": Service.CONFIG,
    "Display_CompanyImage": Service.CONFIG,
    "Display_CompanySetup": Service.CONFIG,
    "Display_DashboardConfiguration": Service.CONFIG,
    "Display_DigitalSignatureSetup": Service.CONFIG,
    "Display_DocumentApprovalSetup": Service.CONFIG,
    "Display_DocumentGeneralSetup": Service.CONFIG,
    "Display_DocumentNumberingSetup": Service.CONFIG,
    "Display_EmailSMSSetup": Service.CONFIG,
    "Display_GhanaTaxcodeMapping": Service.CONFIG,
    "Display_HROtherSetup": Service.CONFIG,
    "Display_HROvertimeSetup": Service.CONFIG,
    "Display_HRPerquisiteSetup": Service.CONFIG,
    "Display_HRSalarySetup": Service.CONFIG,
    "Display_HRStatutorySetup": Service.CONFIG,
    "Display_Integration_Config": Service.CONFIG,
    "Display_MasterApprovalConfiguration": Service.CONFIG,
    "Display_PrintConfiguration": Service.CONFIG,
    "Display_ScheduleConfiguration": Service.CONFIG,
    "Display_UserPermission": Service.CONFIG,
    "GetCompaniesListofEnterprise": Service.CONFIG,
    "GetDashboardConfig": Service.CONFIG,
    "GetObjectRights": Service.CONFIG,
    "GetPasswordPolicy": Service.CONFIG,
    "SaveAuthoriseCompanyToPullData": Service.CONFIG,
    "SaveChildCompanyVsCustomerMapping": Service.CONFIG,
    "SaveDocumentApprovalConfiguration": Service.CONFIG,
    "SaveEmail_SMSConfiguration": Service.CONFIG,
    "SaveUnmappedItemAccrossCompany": Service.CONFIG,
    "SaveUpdate_DashboardConfiguration": Service.CONFIG,
    "SaveUpdate_DigitalSignatureSetup": Service.CONFIG,
    "SaveUpdate_DocumentGeneralSetup": Service.CONFIG,
    "SaveUpdate_DocumentNumberingSetup": Service.CONFIG,
    "SaveUpdate_HROtherSetup": Service.CONFIG,
    "SaveUpdate_HROvertimeSetup": Service.CONFIG,
    "SaveUpdate_HRPerquisiteSetup": Service.CONFIG,
    "SaveUpdate_HRSalarySetup": Service.CONFIG,
    "SaveUpdate_HRStatutorySetup": Service.CONFIG,
    "SaveUpdate_Integration_Config": Service.CONFIG,
    "SaveUpdate_PrintConfiguration": Service.CONFIG,
    "SaveUpdate_ScheduleConfiguration": Service.CONFIG,
    "SaveUpdate_UserPermission": Service.CONFIG,
    "SaveUserMenuRights": Service.CONFIG,
    "Save_ApprovalAdvancement": Service.CONFIG,
    "Save_GhanaTaxcodeMapping": Service.CONFIG,
    "Save_MasterApprovalConfiguration": Service.CONFIG,
    "Update_CompanyBasicSetup": Service.CONFIG,
    "Update_CompanyFinanceSetup": Service.CONFIG,
    "Update_CompanyGeneralSetup": Service.CONFIG,
    "Update_CompanyGeneralSetup_LockUpto": Service.CONFIG,
    "Update_CompanyInventorySetup": Service.CONFIG,
    "Update_CompanyPurchaseSetup": Service.CONFIG,
    "Update_CompanySalesSetup": Service.CONFIG,
    "Update_DefaultGL": Service.CONFIG,
    "Update_Integration_ConfigStatus": Service.CONFIG,

    # ── ABEnterpriseService.svc (23 endpoints)
    "ABCRM_IVR_ClickToCall": Service.ENTERPRISE,
    "CRMTrn_GetTopicForTrainingFeedback": Service.ENTERPRISE,
    "CRMTrn_SaveTrainingFeedback": Service.ENTERPRISE,
    "CreateCompany": Service.ENTERPRISE,
    "CreateGuestUser": Service.ENTERPRISE,
    "DeleteCompany": Service.ENTERPRISE,
    "GetCRMReport": Service.ENTERPRISE,
    "GetClientListForUser": Service.ENTERPRISE,
    "GetLicenseInfoForEnterprise": Service.ENTERPRISE,
    "GetSubscriptionInfo": Service.ENTERPRISE,
    "IVR_ClickToCall": Service.ENTERPRISE,
    "InAppFeedbackFromMobile": Service.ENTERPRISE,
    "ListSalesPartner": Service.ENTERPRISE,
    "ProcessURL": Service.ENTERPRISE,
    "SaveLicenseOrder": Service.ENTERPRISE,
    "Save_Survey": Service.ENTERPRISE,
    "UpdateEnterpriseOffer": Service.ENTERPRISE,
    "UpdateLicenseOrderStatus": Service.ENTERPRISE,
    "UpdateUserProfile": Service.ENTERPRISE,
    "ValidateGuestUserInCompany": Service.ENTERPRISE,
    "ValidateURL": Service.ENTERPRISE,
    "VerifyUniqueUser": Service.ENTERPRISE,
    "support_SaveSupportTicket": Service.ENTERPRISE,

    # ── ABImportService.svc (11 endpoints)
    "Delete_ExcelColumnMapping": Service.IMPORT,
    "Display_ExcelColumnMapping": Service.IMPORT,
    "ExportVoucherToExcel": Service.IMPORT,
    "GetIPAddress": Service.IMPORT,
    "ImportFromSAP": Service.IMPORT,
    "Import_Master": Service.IMPORT,
    "Save_ExcelColumnMapping": Service.IMPORT,
    "WhatsAppWeb_MobileLinkage": Service.IMPORT,
    "WhatsAppWeb_PurchasePlan": Service.IMPORT,
    "WhatsAppWeb_Register": Service.IMPORT,
    "WhatsAppWeb_StatusChecking": Service.IMPORT,

    # ── ABReportService.svc (31 endpoints)
    "DeleteReportFromFavourite": Service.REPORT,
    "DeleteView": Service.REPORT,
    "DisplayCustomReport": Service.REPORT,
    "DownloadEInvoiceJson": Service.REPORT,
    "DownloadEWayBillJson": Service.REPORT,
    "DownloadFTAVATAuditFile": Service.REPORT,
    "GenerateLoanAccountConfirmation": Service.REPORT,
    "GenerateOTPGSTR": Service.REPORT,
    "GeneratePartyAccountConfirmation": Service.REPORT,
    "GeneratePaySlip": Service.REPORT,
    "GeneratePaymentReminder": Service.REPORT,
    "GetCalculativeColumns": Service.REPORT,
    "GetFavouriteReportMenu": Service.REPORT,
    "GetGSTR": Service.REPORT,
    "GetReportData": Service.REPORT,
    "GetReportFilter": Service.REPORT,
    "GetReportPrintExportDetailToExcel": Service.REPORT,
    "GetReportPrintExportDetailToNotepad": Service.REPORT,
    "GetReportPrintPDF": Service.REPORT,
    "GetReportView": Service.REPORT,
    "GetStockStatementForBank": Service.REPORT,
    "GetUserReportColumn": Service.REPORT,
    "GetVATReturn_MiddleEastJson": Service.REPORT,
    "GetVoucerListForFilter": Service.REPORT,
    "ListReportView": Service.REPORT,
    "SaveCustomReport": Service.REPORT,
    "SaveReportInFavourite": Service.REPORT,
    "SaveUserReportCalculativeColumn": Service.REPORT,
    "SaveUserReportColumn": Service.REPORT,
    "SetAsDefaultView": Service.REPORT,
    "UploadGSTR": Service.REPORT,

    # ── ABUtilityService.svc (32 endpoints)
    "ChangePassword": Service.UTILITY,
    "ContactManagementSendEmailSMS": Service.UTILITY,
    "DeleteFavouriteMenu": Service.UTILITY,
    "GetCompanySelectionList": Service.UTILITY,
    "GetCompleteCurrencyList": Service.UTILITY,
    "GetDataForQuery": Service.UTILITY,
    "GetDocumentPrint": Service.UTILITY,
    "GetDocumentURLInfo": Service.UTILITY,
    "GetFavouriteMenu": Service.UTILITY,
    "GetFilterForQuery": Service.UTILITY,
    "GetFinancialPeriodList": Service.UTILITY,
    "GetLinkageParent": Service.UTILITY,
    "GetMasterCode": Service.UTILITY,
    "GetSampleDocumentPreview": Service.UTILITY,
    "GetVideoLink": Service.UTILITY,
    "GetVoucherNumber": Service.UTILITY,
    "ICICINewAccountRequest": Service.UTILITY,
    "PickPackSendEmailSMS": Service.UTILITY,
    "QueryExecute": Service.UTILITY,
    "ResendCommunication": Service.UTILITY,
    "ResetCompanyStatic": Service.UTILITY,
    "SaveFavouriteMenu": Service.UTILITY,
    "SendForgotPasswordOTP": Service.UTILITY,
    "SendReport": Service.UTILITY,
    "SendVoucherEmail": Service.UTILITY,
    "SendVoucherMailLink": Service.UTILITY,
    "SendVoucherSMS": Service.UTILITY,
    "SendWhatsAppMessage": Service.UTILITY,
    "TextToSpeech": Service.UTILITY,
    "UpdateCustomerRemark": Service.UTILITY,
    "UpdateDefaultCompany": Service.UTILITY,
    "ValidatePasswordPolicy": Service.UTILITY,
}

# ── Indian States GST codes ──────────────────────────────────────────────────
INDIAN_STATES: dict[str, str] = {
    "01": "Jammu & Kashmir", "02": "Himachal Pradesh", "03": "Punjab",
    "04": "Chandigarh", "05": "Uttarakhand", "06": "Haryana",
    "07": "Delhi", "08": "Rajasthan", "09": "Uttar Pradesh",
    "10": "Bihar", "11": "Sikkim", "12": "Arunachal Pradesh",
    "13": "Nagaland", "14": "Manipur", "15": "Mizoram",
    "16": "Tripura", "17": "Meghalaya", "18": "Assam",
    "19": "West Bengal", "20": "Jharkhand", "21": "Odisha",
    "22": "Chhattisgarh", "23": "Madhya Pradesh", "24": "Gujarat",
    "26": "Dadra & Nagar Haveli and Daman & Diu", "27": "Maharashtra",
    "28": "Andhra Pradesh (new)", "29": "Karnataka", "30": "Goa",
    "31": "Lakshadweep", "32": "Kerala", "33": "Tamil Nadu",
    "34": "Puducherry", "35": "Andaman & Nicobar Islands",
    "36": "Telangana", "37": "Andhra Pradesh (old)", "38": "Ladakh",
    "97": "Other Territory", "99": "Centre Jurisdiction",
}

# ── Save body key mapping ──────────────────────────────────────────────────
# Some SaveUpdate_* endpoints use different body key than "info"
SAVE_BODY_KEY: dict[str, str] = {
    "SaveUpdate_Invoice":               "invoice",
    "SaveUpdate_Order":                 "info",
    "SaveUpdate_Item":                  "item_information",
    "SaveUpdate_Party":                 "info",
    "SaveUpdate_Ledger":                "info",
    "SaveUpdate_JournalVoucher":        "info",
    "SaveUpdate_PaymentReceiptVoucher": "info",
    "SaveUpdate_Estimate":              "info",
    "SaveUpdate_Challan":               "info",
    "SaveUpdate_MaterialAdjustment":    "info",
    "SaveUpdate_Jobwork":               "info",
    "SaveUpdate_InterBranch":           "info",
    "SaveUpdate_BOMBasedProduction":    "info",
    "SaveUpdate_ExpenseJournalVoucher": "info",
    "SaveUpdate_PurchaseRequisition":   "info",
}
