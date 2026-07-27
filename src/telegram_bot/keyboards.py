from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def ceo_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")
        ],
        [
            InlineKeyboardButton("📦 Inventory", callback_data="inventory")
        ],
        [
            InlineKeyboardButton("💰 Finance", callback_data="finance")
        ],
        [
            InlineKeyboardButton("👥 Customers", callback_data="customers")
        ],
        [
            InlineKeyboardButton("⚙ Settings", callback_data="settings")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
