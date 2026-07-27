from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def settings_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔐 Security",
                callback_data="security_center"
            )
        ],
        [
            InlineKeyboardButton(
                "👥 Users",
                callback_data="manage_users"
            )
        ],
        [
            InlineKeyboardButton(
                "🏢 Business Profile",
                callback_data="business_profile"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="dashboard"
            )
        ]
    ])
