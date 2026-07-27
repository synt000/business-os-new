from telegram import Update
from telegram.ext import ContextTypes


async def inventory_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "📦 *Inventory Center*\n\n"
        "Stock\n"
        "Movements\n"
        "Warehouse Analysis Ready ✅",
        parse_mode="Markdown"
    )
