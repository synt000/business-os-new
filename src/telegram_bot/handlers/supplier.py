from telegram import Update
from telegram.ext import ContextTypes


async def supplier_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🏭 *Business OS Suppliers*\n\n"
        "🏢 Total Suppliers: Loading...\n"
        "📦 Purchase Flow: Ready...",
        parse_mode="Markdown"
    )
