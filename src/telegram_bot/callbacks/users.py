from telegram import Update
from telegram.ext import ContextTypes
from src.telegram_bot.keyboards import users_center_menu


async def users_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "👥 *User Management Center*\n\n"
        "RBAC Engine Active ✅\n"
        "User Permissions Ready 🔐",
        parse_mode="Markdown",
        reply_markup=users_center_menu()
    )
