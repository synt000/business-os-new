from telegram import Update
from telegram.ext import ContextTypes


async def security_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "🔐 *Security Center*\n\n"
        "Role Management\n"
        "User Access Control\n"
        "Audit Logs Ready ✅",
        parse_mode="Markdown"
    )
