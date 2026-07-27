from telegram import Update
from telegram.ext import ContextTypes


async def finance_revenue_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📈 *Revenue Analysis*\n\n"
        "Total Revenue Data Ready ✅",
        parse_mode="Markdown"
    )


async def finance_expense_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "💸 *Expense Center*\n\n"
        "Expense Tracking Ready ✅",
        parse_mode="Markdown"
    )


async def finance_profit_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "💰 *Profit Analysis*\n\n"
        "Profit Engine Ready ✅",
        parse_mode="Markdown"
    )
