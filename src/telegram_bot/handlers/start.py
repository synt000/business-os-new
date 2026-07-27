from telegram import Update
from telegram.ext import ContextTypes


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    print(
        "🚀 TELEGRAM /start RECEIVED:",
        update.effective_user.id,
        update.effective_user.username
    )

    await update.message.reply_text(
        """
🤖 Business OS CEO Bot Online

Welcome Bro.

📊 Dashboard
💰 Finance
📦 Inventory
👥 Customers

System Connected Successfully.
"""
    )
