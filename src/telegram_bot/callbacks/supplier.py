from telegram import Update
from telegram.ext import ContextTypes
from src.telegram_bot.keyboards import supplier_menu


async def supplier_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "🏭 *Supplier Center*\n\n"
        "Select Supplier Module:",
        parse_mode="Markdown",
        reply_markup=supplier_menu()
    )
