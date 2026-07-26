from src.models.saas_core import BusinessFeature


MENU_MAP = {

    "PRODUCT": {
        "name": "📦 Product",
        "url": "/products/ui",
        "roles": ["OWNER","MANAGER","STAFF"]
    },

    "INVENTORY": {
        "name": "📊 Inventory",
        "url": "/inventory/ui",
        "roles": ["OWNER","MANAGER","STAFF"]
    },

    "ORDER": {
        "name": "🛒 Orders",
        "url": "/orders/ui",
        "roles": ["OWNER","MANAGER","STAFF"]
    },

    "CUSTOMER": {
        "name": "👥 Customers",
        "url": "/customers/ui",
        "roles": ["OWNER","MANAGER","STAFF"]
    },

    "PAYMENT": {
        "name": "💰 Payment",
        "url": "/payment/ui",
        "roles": ["OWNER","MANAGER"]
    },

    "DELIVERY": {
        "name": "🚚 Delivery",
        "url": "/delivery/ui",
        "roles": ["OWNER","MANAGER","STAFF"]
    },

    "PROMOTION": {
        "name": "🎯 Promotion",
        "url": "/promotion/ui",
        "roles": ["OWNER","MANAGER"]
    },

    "SOCIAL_MEDIA": {
        "name": "📱 Social Media",
        "url": "/social/ui",
        "roles": ["OWNER","MANAGER"]
    },

    "BOOKING": {
        "name": "📅 Booking",
        "url": "/booking/ui",
        "roles": ["OWNER","MANAGER","STAFF"]
    },

    "STAFF": {
        "name": "👨‍💼 Staff",
        "url": "/staff/ui",
        "roles": ["OWNER","MANAGER"]
    },

    "REPORT": {
        "name": "📈 Reports",
        "url": "/reports/ui",
        "roles": ["OWNER","MANAGER"]
    }
}


def get_sidebar_menu(db, business_type_id, role="OWNER"):

    features = (
        db.query(BusinessFeature)
        .filter(
            BusinessFeature.business_type_id == business_type_id,
            BusinessFeature.enabled == True
        )
        .all()
    )

    menu = []

    for feature in features:

        item = MENU_MAP.get(feature.feature_code)

        if item and role in item["roles"]:
            menu.append(item)

    return menu
