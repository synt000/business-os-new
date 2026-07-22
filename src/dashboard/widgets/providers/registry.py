from src.dashboard.widgets.providers.sales import sales_widget
from src.dashboard.widgets.providers.social import social_widget
from src.dashboard.widgets.providers.products import top_products_widget
from src.dashboard.widgets.providers.packing import packing_pending_widget
from src.dashboard.widgets.providers.delivery import delivery_pending_widget
from src.dashboard.widgets.providers.cod import cod_collection_widget
from src.dashboard.widgets.providers.inventory import inventory_widget
from src.dashboard.widgets.providers.low_stock import low_stock_widget
from src.dashboard.widgets.providers.profit import profit_widget
from src.dashboard.widgets.providers.ad_roi import ad_roi_widget
from src.dashboard.widgets.providers.customer import customer_widget
from src.dashboard.widgets.providers.receivable import receivable_widget

from src.dashboard.widgets.providers.retail_wholesale import (
    total_sales_widget,
    gross_profit_widget,
    retail_wholesale_ratio_widget,
    average_ticket_widget,
    inventory_value_widget,
    wholesale_ledger_widget,
    customer_credit_widget,
    supplier_debt_widget,
    purchase_orders_widget,
    b2b_billing_widget,
    retail_pos_widget,
    bulk_price_widget,
    stock_in_grn_widget,
)

from src.dashboard.widgets.providers.beauty_salon import (
    appointments_widget,
    staff_schedule_widget,
    services_sold_widget,
    customer_return_rate_widget,
    top_staff_widget,
    product_sales_widget,
    revenue_widget,
    no_show_rate_widget,
    back_bar_inventory_widget,
    walk_in_checkout_widget,
)

from src.dashboard.widgets.providers.mini_mart import (
    fast_moving_items_widget,
    supplier_debt_widget,
    daily_profit_widget,
    total_revenue_widget,
    payment_methods_widget,
    customer_debt_widget,
    expiry_alert_widget,
    dead_stock_widget,
    pos_terminal_widget,
)

from src.dashboard.widgets.providers.two_d import (
    two_d_result_widget,
    commission_widget,
    agent_sales_widget,
    winning_numbers_widget,
    hot_numbers_widget,
    ticket_sales_widget,
    agent_management_widget,
    financial_ledger_widget,
)


WIDGET_PROVIDERS = {
    "sales": sales_widget,
    "social": social_widget,
    "delivery_pending": delivery_pending_widget,
    "cod_collection": cod_collection_widget,
    "top_products": top_products_widget,
    "inventory": inventory_widget,
    "low_stock": low_stock_widget,
    "profit": profit_widget,
    "packing_pending": packing_pending_widget,
    "parcel_tracking": delivery_pending_widget,
    "ad_roi": ad_roi_widget,
    "customer": customer_widget,
    "receivable": receivable_widget,

    # TWO_D_SELLER
    "two_d_result": two_d_result_widget,
    "commission": commission_widget,
    "agent_sales": agent_sales_widget,
    "winning_numbers": winning_numbers_widget,
    "hot_numbers": hot_numbers_widget,
    "ticket_sales": ticket_sales_widget,
    "agent_management": agent_management_widget,
    "financial_ledger": financial_ledger_widget,

    # MINI_MART
    "fast_moving_items": fast_moving_items_widget,
    "supplier_debt": supplier_debt_widget,
    "daily_profit": daily_profit_widget,
    "total_revenue": total_revenue_widget,
    "payment_methods": payment_methods_widget,
    "customer_debt": customer_debt_widget,
    "expiry_alert": expiry_alert_widget,
    "dead_stock": dead_stock_widget,
    "pos_terminal": pos_terminal_widget,

    # BEAUTY_SALON
    "appointments": appointments_widget,
    "staff_schedule": staff_schedule_widget,
    "services_sold": services_sold_widget,
    "customer_return_rate": customer_return_rate_widget,
    "top_staff": top_staff_widget,
    "product_sales": product_sales_widget,
    "revenue": revenue_widget,
    "no_show_rate": no_show_rate_widget,
    "back_bar_inventory": back_bar_inventory_widget,
    "walk_in_checkout": walk_in_checkout_widget,

    # RETAIL_WHOLESALE
    "total_sales": total_sales_widget,
    "gross_profit": gross_profit_widget,
    "retail_wholesale_ratio": retail_wholesale_ratio_widget,
    "average_ticket": average_ticket_widget,
    "inventory_value": inventory_value_widget,
    "wholesale_ledger": wholesale_ledger_widget,
    "customer_credit": customer_credit_widget,
    "supplier_debt": supplier_debt_widget,
    "purchase_orders": purchase_orders_widget,
    "b2b_billing": b2b_billing_widget,
    "retail_pos": retail_pos_widget,
    "bulk_price": bulk_price_widget,
    "stock_in_grn": stock_in_grn_widget,
}


def get_widget_provider(name):
    return WIDGET_PROVIDERS.get(name)


def validate_widgets(widget_names):
    return {
        name: (
            "AVAILABLE"
            if name in WIDGET_PROVIDERS
            else "MISSING_PROVIDER"
        )
        for name in widget_names
    }
