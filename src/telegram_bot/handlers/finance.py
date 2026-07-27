from telegram import Update
from telegram.ext import ContextTypes


async def finance_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "💰 *Business OS Finance*\n\n"
        "Revenue: Loading...\n"
        "Expense: Loading...\n"
        "Profit: Loading...",
        parse_mode="Markdown"
    )
