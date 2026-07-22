from pathlib import Path

p = Path("src/dashboard/widgets/providers/registry.py")

s = p.read_text()

s = s.replace(
    "from src.dashboard.widgets.providers.social import social_widget",
    "from src.dashboard.widgets.providers.social import social_widget\nfrom src.dashboard.widgets.providers.products import top_products_widget"
)

s = s.replace(
    '"tiktok_orders": social_widget,',
    '"tiktok_orders": social_widget,\n    "top_products": top_products_widget,'
)

p.write_text(s)

print("registry updated")
