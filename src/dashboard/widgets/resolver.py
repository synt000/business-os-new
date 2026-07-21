"""
Dashboard Widget Resolver

Returns dashboard widgets by business type
"""

from src.dashboard.widgets.config import (
    BUSINESS_DASHBOARD_WIDGETS
)


def get_dashboard_widgets(business_type: str):

    if not business_type:
        return []

    business_type = business_type.upper()

    return BUSINESS_DASHBOARD_WIDGETS.get(
        business_type,
        []
    )
