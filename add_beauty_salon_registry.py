from pathlib import Path

p = Path("src/dashboard/widgets/providers/registry.py")

s = p.read_text()

if "providers.beauty_salon import" not in s:
    s = s.replace(
        "from src.dashboard.widgets.providers.mini_mart import (",
        """from src.dashboard.widgets.providers.beauty_salon import (
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

from src.dashboard.widgets.providers.mini_mart import ("""
    )

if '"appointments": appointments_widget' not in s:
    s = s.replace(
        '    "pos_terminal": pos_terminal_widget,\n',
        '''    "pos_terminal": pos_terminal_widget,

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
'''
    )

p.write_text(s)

print("beauty salon registry updated")
