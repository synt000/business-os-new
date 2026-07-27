from telegram import Update
from telegram.ext import ContextTypes


async def finance_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "💰 *Finance Center*\n\n"
        "Revenue\n"
        "Expense\n"
        "Profit Analysis Ready ✅",
        parse_mode="Markdown"
    )
