from telegram import Update
from telegram.ext import ContextTypes
from src.telegram_bot.keyboards import dashboard_menu


async def dashboard_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "📊 *Dashboard*\n\n"
        "Live Business Overview Ready ✅",
        parse_mode="Markdown",
        reply_markup=dashboard_menu()
    )
