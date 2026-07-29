"""
Dashboard Widget Resolver

Returns dashboard widgets by business type
"""

from src.dashboard.widgets.config import (
    BUSINESS_DASHBOARD_WIDGETS
)


BUSINESS_TYPE_ALIAS = {
    "RETAIL": "RETAIL_WHOLESALE",
}


def get_dashboard_widgets(business_type: str):

    if not business_type:
        return []

    business_type = business_type.upper()

    business_type = BUSINESS_TYPE_ALIAS.get(
        business_type,
        business_type
    )

    return BUSINESS_DASHBOARD_WIDGETS.get(
        business_type,
        []
    )
