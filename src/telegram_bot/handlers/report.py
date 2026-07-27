from telegram import Update
from telegram.ext import ContextTypes


async def report_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📊 *Business OS Reports*\n\n"
        "📈 Sales Report: Loading...\n"
        "💰 Finance Report: Loading...\n"
        "📦 Inventory Report: Loading...",
        parse_mode="Markdown"
    )
