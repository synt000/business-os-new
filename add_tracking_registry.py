from pathlib import Path

p = Path("src/dashboard/widgets/providers/registry.py")

s = p.read_text()

if "parcel_tracking_widget" not in s:
    s = s.replace(
        "from src.dashboard.widgets.providers.inventory import inventory_widget",
        "from src.dashboard.widgets.providers.inventory import inventory_widget\nfrom src.dashboard.widgets.providers.tracking import parcel_tracking_widget"
    )

    s = s.replace(
        '"inventory": inventory_widget,',
        '"inventory": inventory_widget,\n    "parcel_tracking": parcel_tracking_widget,'
    )

    p.write_text(s)

print("tracking registry updated")
