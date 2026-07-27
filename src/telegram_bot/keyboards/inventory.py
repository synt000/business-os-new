from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def inventory_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📦 Stock Overview",
                callback_data="inventory_stock"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Stock Movements",
                callback_data="inventory_movements"
            )
        ],
        [
            InlineKeyboardButton(
                "🏭 Warehouse Analysis",
                callback_data="inventory_warehouse"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="dashboard"
            )
        ]
    ])
