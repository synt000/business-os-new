from telegram import Update
from telegram.ext import ContextTypes


async def dashboard_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📊 *Business OS Dashboard*\n\n"
        "📦 Products: Loading...\n"
        "💰 Revenue: Loading...\n"
        "📈 Profit: Loading...\n"
        "⚠ Alerts: None",
        parse_mode="Markdown"
    )
