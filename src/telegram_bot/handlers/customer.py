from telegram import Update
from telegram.ext import ContextTypes


async def customer_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "👥 *Business OS Customers*\n\n"
        "👤 Total Customers: Loading...\n"
        "📝 Recent Customers: Loading...",
        parse_mode="Markdown"
    )
