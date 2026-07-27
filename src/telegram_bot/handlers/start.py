from telegram import Update
from telegram.ext import ContextTypes

from src.telegram_bot.keyboards import ceo_main_menu


async def start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🤖 *Business OS CEO*\n\n"
        "Welcome Owner ✅",
        parse_mode="Markdown",
        reply_markup=ceo_main_menu()
    )
