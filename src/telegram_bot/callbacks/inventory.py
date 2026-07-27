from telegram import Update
from telegram.ext import ContextTypes
from src.telegram_bot.keyboards import inventory_menu


async def inventory_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "📦 *Inventory Center*\n\n"
        "Select Inventory Module:",
        parse_mode="Markdown",
        reply_markup=inventory_menu()
    )
