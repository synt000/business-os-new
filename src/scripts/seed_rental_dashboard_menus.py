from src.core.database import SessionLocal
from src.models.saas_core import DashboardMenu


db = SessionLocal()

menus = [
    ("RENTAL_ITEM", "Rental Items", "box", "/rental/items"),
    ("RENTAL_BOOKING", "Rental Booking", "calendar", "/rental/bookings"),
    ("CUSTOMER", "Customers", "users", "/customers"),
    ("PAYMENT", "Payments", "credit-card", "/payments"),
    ("DEPOSIT", "Deposits", "wallet", "/rental/deposits"),
    ("RETURN_TRACKING", "Return Tracking", "rotate", "/rental/returns"),
    ("MAINTENANCE", "Maintenance", "tool", "/rental/maintenance"),
    ("INVOICE", "Invoices", "file-text", "/invoices"),
    ("INVENTORY", "Inventory", "archive", "/inventory"),
    ("LOG_HISTORY", "History", "history", "/logs"),
]


for feature_code, menu_name, icon, route in menus:

    exists = (
        db.query(DashboardMenu)
        .filter(
            DashboardMenu.feature_code == feature_code
        )
        .first()
    )

    if not exists:
        db.add(
            DashboardMenu(
                feature_code=feature_code,
                menu_name=menu_name,
                menu_icon=icon,
                route_path=route
            )
        )


db.commit()
db.close()

print("✓ Rental Dashboard Menus Seeded")
