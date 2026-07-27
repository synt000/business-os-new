from telegram import Update
from telegram.ext import ContextTypes


async def settings_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "⚙️ *Settings Center*\n\n"
        "🔐 Security\n"
        "👥 Users\n"
        "🏢 Business Profile Ready ✅",
        parse_mode="Markdown"
    )
