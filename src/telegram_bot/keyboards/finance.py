from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def finance_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📈 Revenue",
                callback_data="finance_revenue"
            )
        ],
        [
            InlineKeyboardButton(
                "💸 Expense",
                callback_data="finance_expense"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Profit Analysis",
                callback_data="finance_profit"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="dashboard"
            )
        ]
    ])
