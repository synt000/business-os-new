from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def user_detail_keyboard(user_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔐 Change Role",
                callback_data=f"change_role_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🚫 Disable User",
                callback_data=f"disable_user_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔑 Reset Password",
                callback_data=f"reset_password_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "📜 Activity Logs",
                callback_data=f"activity_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="view_users"
            )
        ]
    ])
