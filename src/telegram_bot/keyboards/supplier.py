from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def supplier_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏭 Supplier List",
                callback_data="supplier_list"
            )
        ],
        [
            InlineKeyboardButton(
                "➕ Add Supplier",
                callback_data="supplier_add"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Supplier Analysis",
                callback_data="supplier_analysis"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="dashboard"
            )
        ]
    ])
