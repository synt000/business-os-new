from telegram import Update
from telegram.ext import ContextTypes
from src.telegram_bot.keyboards import report_menu


async def report_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "📊 *Report Center*\n\n"
        "Select Report Type:",
        parse_mode="Markdown",
        reply_markup=report_menu()
    )
