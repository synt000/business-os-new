from src.core.database import SessionLocal

from src.models.saas_core import DashboardMenu

import uuid


db = SessionLocal()


menus = [

("ORDER","Orders","🛒","/orders"),
("CUSTOMER","Customers","👥","/customers"),
("PAYMENT","Payments","💳","/payments"),
("DELIVERY","Delivery","🚚","/delivery"),
("PROMOTION","Marketing","🎯","/marketing"),
("INVENTORY","Inventory","🏬","/inventory"),
("PURCHASE","Purchase","🧾","/purchase"),
("SUPPLIER","Suppliers","🏭","/suppliers"),
("POS","POS","🧮","/pos"),
("BOOKING","Appointments","📅","/booking"),
("STAFF","Staff","👨‍💼","/staff"),
("SERVICE_PACKAGE","Services","💇","/services"),
("DESIGN_SERVICE","Design Service","🎨","/design"),
("FILE_DELIVERY","Files","📁","/files"),
("LOG_HISTORY","History","📜","/logs"),

]


for code,name,icon,route in menus:

    exists = (
        db.query(DashboardMenu)
        .filter(
            DashboardMenu.feature_code == code
        )
        .first()
    )

    if not exists:

        db.add(
            DashboardMenu(
                id=str(uuid.uuid4()),
                feature_code=code,
                menu_name=name,
                menu_icon=icon,
                route_path=route
            )
        )


db.commit()

db.close()


print("✓ Dashboard Menus Seeded")
