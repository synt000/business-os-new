from telegram import Update
from telegram.ext import ContextTypes
from src.telegram_bot.keyboards import customer_menu


async def customer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "👥 *Customer Center*\n\n"
        "Select Customer Module:",
        parse_mode="Markdown",
        reply_markup=customer_menu()
    )
