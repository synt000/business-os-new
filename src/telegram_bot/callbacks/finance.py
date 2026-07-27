from telegram import Update
from telegram.ext import ContextTypes
from src.telegram_bot.keyboards import finance_menu


async def finance_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "💰 *Finance Center*\n\n"
        "Select Finance Module:",
        parse_mode="Markdown",
        reply_markup=finance_menu()
    )
