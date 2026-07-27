from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def report_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📊 Sales Report",
                callback_data="sales_report"
            )
        ],
        [
            InlineKeyboardButton(
                "📦 Inventory Report",
                callback_data="inventory_report"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Finance Report",
                callback_data="finance_report"
            )
        ]
    ])
