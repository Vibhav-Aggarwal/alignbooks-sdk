"""Reporting services: dashboard, GST, analytics."""

from __future__ import annotations

from typing import Any

from ._base import BaseService


class ReportsService(BaseService):
    """Report operations."""

    def dashboard(self) -> dict[str, Any]:
        """Get dashboard key figures data."""
        return self._call("GetDashboardKeyFiguresDataList")

    def dashboard_widgets(self) -> dict[str, Any]:
        """Get dashboard widget data."""
        return self._call("GetDashboardWidgetDataList")
