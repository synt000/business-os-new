from pathlib import Path

p = Path("src/dashboard/widgets/providers/registry.py")

s = p.read_text()

if "packing_pending_widget" not in s:
    s = s.replace(
        "from src.dashboard.widgets.providers.products import top_products_widget",
        "from src.dashboard.widgets.providers.products import top_products_widget\nfrom src.dashboard.widgets.providers.packing import packing_pending_widget"
    )

    s = s.replace(
        '"top_products": top_products_widget,',
        '"top_products": top_products_widget,\n    "packing_pending": packing_pending_widget,'
    )

    p.write_text(s)

print("packing registry updated")
