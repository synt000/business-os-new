from src.dashboard.widgets.resolver import get_dashboard_widgets
from src.dashboard.widgets.providers.registry import get_widget_provider


def resolve_widget_data(
    business_type,
    db,
    tenant_id
):

    widget_names = get_dashboard_widgets(
        business_type
    )

    result = {}

    for name in widget_names:

        provider = get_widget_provider(name)

        if provider:
            try:
                result[name] = provider(
                    db,
                    tenant_id
                )
            except Exception as e:
                result[name] = {
                    "status": "ERROR",
                    "message": str(e)
                }

        else:
            result[name] = {
                "status": "NOT_IMPLEMENTED"
            }

    return result
