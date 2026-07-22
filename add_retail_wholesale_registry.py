from pathlib import Path

p = Path("src/dashboard/widgets/providers/registry.py")

s = p.read_text()

if "providers.retail_wholesale import" not in s:
    s = s.replace(
        "from src.dashboard.widgets.providers.beauty_salon import (",
        """from src.dashboard.widgets.providers.retail_wholesale import (
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

from src.dashboard.widgets.providers.beauty_salon import ("""
    )

if '"total_sales": total_sales_widget' not in s:
    s = s.replace(
        '    "walk_in_checkout": walk_in_checkout_widget,\n',
        '''    "walk_in_checkout": walk_in_checkout_widget,

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
'''
    )

p.write_text(s)

print("retail wholesale registry updated")
