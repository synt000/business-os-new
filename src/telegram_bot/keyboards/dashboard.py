from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def dashboard_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📊 Live Summary",
                callback_data="dashboard_summary"
            )
        ],
        [
            InlineKeyboardButton(
                "📈 Analytics",
                callback_data="dashboard_analytics"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="dashboard"
            )
        ]
    ])
