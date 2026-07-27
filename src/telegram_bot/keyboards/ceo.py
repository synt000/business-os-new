from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def ceo_main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👥 Manage Users",
                callback_data="manage_users"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Dashboard",
                callback_data="dashboard"
            )
        ],
        [
            InlineKeyboardButton(
                "📦 Inventory",
                callback_data="inventory"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Finance",
                callback_data="finance"
            )
        ],
        [
            InlineKeyboardButton(
                "👤 Customers",
                callback_data="customer"
            )
        ],
        [
            InlineKeyboardButton(
                "🏭 Suppliers",
                callback_data="supplier"
            )
        ],
        [
            InlineKeyboardButton(
                "📑 Reports",
                callback_data="report"
            )
        ],
        [
            InlineKeyboardButton(
                "⚙️ Settings",
                callback_data="settings"
            )
        ]
    ])
