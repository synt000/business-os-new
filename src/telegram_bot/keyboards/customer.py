from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def customer_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👥 Customer List",
                callback_data="customer_list"
            )
        ],
        [
            InlineKeyboardButton(
                "➕ Add Customer",
                callback_data="customer_add"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Customer Analysis",
                callback_data="customer_analysis"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="dashboard"
            )
        ]
    ])
