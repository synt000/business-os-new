from pathlib import Path

p = Path("src/dashboard/widgets/providers/registry.py")

s = p.read_text()

# import block
if "from src.dashboard.widgets.providers.mini_mart import" not in s:
    s = s.replace(
        "from src.dashboard.widgets.providers.two_d import (",
        """from src.dashboard.widgets.providers.mini_mart import (
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

from src.dashboard.widgets.providers.two_d import ("""
    )

# provider registry block
if '"fast_moving_items": fast_moving_items_widget' not in s:
    s = s.replace(
        '    "financial_ledger": financial_ledger_widget,\n',
        '''    "financial_ledger": financial_ledger_widget,

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
'''
    )

p.write_text(s)

print("mini mart registry updated")
