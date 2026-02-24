"""Main AlignBooks API client.

Provides a high-level interface for making authenticated API calls to AlignBooks.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import requests

from .auth import make_ab_token
from .constants import API_BASE, DEFAULT_MASTER_TYPE, SERVICE_MAP, Service
from .exceptions import APIError, AuthenticationError, SessionExpiredError

logger = logging.getLogger("alignbooks")


class AlignBooksClient:
    """Low-level HTTP client for AlignBooks API.

    Handles authentication, token generation, session management, and raw API calls.

    Args:
        email: Login email address.
        password: Login password.
        api_key: AlignBooks API key (GUID).
        enterprise_id: Enterprise ID (GUID).
        company_id: Company ID (GUID).
        user_id: User ID (GUID).
        master_type: Master type code (default 2037).
        base_url: API base URL (default: https://service.alignbooks.com).
        timeout: Request timeout in seconds (default 60).
        auto_login: Automatically login on first API call (default True).

    Example:
        >>> client = AlignBooksClient(
        ...     email="user@example.com",
        ...     password="password",
        ...     api_key="your-api-key",
        ...     enterprise_id="your-enterprise-id",
        ...     company_id="your-company-id",
        ...     user_id="your-user-id",
        ... )
        >>> client.login()
        >>> vendors = client.api_call("ShortList", {"new_id": "00000000-...", "master_type": 2})
    """

    def __init__(
        self,
        email: str,
        password: str,
        api_key: str,
        enterprise_id: str,
        company_id: str,
        user_id: str,
        master_type: int = DEFAULT_MASTER_TYPE,
        base_url: str = API_BASE,
        timeout: int = 60,
        auto_login: bool = True,
    ):
        self.email = email
        self.password = password
        self.api_key = api_key
        self.enterprise_id = enterprise_id
        self.company_id = company_id
        self.user_id = user_id
        self.master_type = master_type
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.auto_login = auto_login

        self._session = requests.Session()
        self._logged_in = False

    def _make_token(self, apiname: str) -> str:
        """Generate ab_token for the given endpoint."""
        return make_ab_token(
            api_key=self.api_key,
            enterprise_id=self.enterprise_id,
            company_id=self.company_id,
            user_id=self.user_id,
            username=self.email,
            password=self.password,
            apiname=apiname,
            master_type=self.master_type,
        )

    def _get_service(self, endpoint: str) -> str:
        """Resolve the service URL suffix for an endpoint."""
        return SERVICE_MAP.get(endpoint, Service.DATA)

    def login(self) -> dict[str, Any]:
        """Establish a server-side session.

        Must be called before most API operations. If auto_login is True,
        this is called automatically on the first API call.

        Returns:
            Login response data.

        Raises:
            AuthenticationError: If login fails.
        """
        result = self.api_call(
            "LoginUser",
            {"login_id": self.email, "password": self.password},
            _skip_auto_login=True,
        )
        self._logged_in = True
        logger.info("Login successful")
        return result

    def api_call(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        service: str | None = None,
        *,
        _skip_auto_login: bool = False,
        _retry_on_session: bool = True,
    ) -> Any:
        """Make an authenticated API call.

        Args:
            endpoint: API endpoint name (e.g. 'ShortList', 'SaveUpdate_Invoice').
            body: Request body dictionary.
            service: Override service URL suffix (auto-detected if not provided).
            _skip_auto_login: Internal flag to prevent login recursion.
            _retry_on_session: Retry with fresh login on session errors.

        Returns:
            Parsed response data. If JsonDataTable contains JSON, it's parsed.
            Otherwise returns the full response dict.

        Raises:
            APIError: If the API returns a non-zero ReturnCode.
            AuthenticationError: If authentication fails.
            SessionExpiredError: If session expired and retry fails.
        """
        if self.auto_login and not self._logged_in and not _skip_auto_login:
            self.login()

        if service is None:
            service = self._get_service(endpoint)

        url = f"{self.base_url}/{service}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "ab_token": self._make_token(endpoint),
        }

        logger.debug("POST %s", url)
        resp = self._session.post(
            url, headers=headers, json=body or {}, timeout=self.timeout
        )
        resp.raise_for_status()

        text = resp.text.lstrip("\ufeff")  # Strip BOM
        data = json.loads(text)

        rc = data.get("ReturnCode", -1)

        # Session expired - retry with fresh login
        if rc == 5000 and _retry_on_session and not _skip_auto_login:
            msg = data.get("Message", "")
            if "Object reference" in msg or "session" in msg.lower():
                logger.info("Session expired, re-logging in...")
                self._logged_in = False
                self.login()
                return self.api_call(
                    endpoint, body, service,
                    _skip_auto_login=False, _retry_on_session=False,
                )

        if rc != 0:
            raise APIError(
                message=data.get("Message", "Unknown error"),
                return_code=rc,
                endpoint=endpoint,
            )

        # Parse JsonDataTable if present
        jdt = data.get("JsonDataTable")
        if jdt:
            try:
                return json.loads(jdt)
            except (json.JSONDecodeError, TypeError):
                return jdt

        return data

    def get_pdf(
        self,
        voucher_id: str,
        vtype: int,
        format_id: str = "",
    ) -> tuple[bytes, str]:
        """Generate and return PDF bytes for a document.

        Args:
            voucher_id: Document/voucher ID (GUID).
            vtype: Document type (VType constant).
            format_id: Print format ID (optional, uses default).

        Returns:
            Tuple of (pdf_bytes, filename).
        """
        body: dict[str, Any] = {
            "voucher_id": voucher_id,
            "vtype": vtype,
            "digital_signature_selected": False,
            "copies": 1,
        }
        if format_id:
            body["format_id"] = format_id

        url = f"{self.base_url}/{Service.UTILITY}/GetDocumentPrint"
        headers = {
            "Content-Type": "application/json",
            "ab_token": self._make_token("GetDocumentPrint"),
        }

        resp = self._session.post(url, headers=headers, json=body, timeout=self.timeout)
        resp.raise_for_status()

        data = json.loads(resp.text.lstrip("\ufeff"))
        if data["ReturnCode"] != 0:
            raise APIError(data.get("Message", ""), data["ReturnCode"], "GetDocumentPrint")

        pdf_bytes = bytes(data["DocumentFile"])
        filename = data.get("JsonDataTableExtn2", "document.pdf")
        return pdf_bytes, filename

    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
