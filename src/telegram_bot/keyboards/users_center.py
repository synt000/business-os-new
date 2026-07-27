from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def users_center_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👥 User List",
                callback_data="users_list"
            )
        ],
        [
            InlineKeyboardButton(
                "🔐 RBAC Roles",
                callback_data="rbac_roles"
            )
        ],
        [
            InlineKeyboardButton(
                "🔑 Permissions",
                callback_data="permissions"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="dashboard"
            )
        ]
    ])
