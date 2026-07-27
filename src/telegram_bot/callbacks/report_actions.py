from telegram import Update
from telegram.ext import ContextTypes


async def sales_report_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📈 *Sales Report*\n\n"
        "Orders Analysis Ready ✅",
        parse_mode="Markdown"
    )


async def inventory_report_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📦 *Inventory Report*\n\n"
        "Stock Analysis Ready ✅",
        parse_mode="Markdown"
    )


async def finance_report_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "💰 *Finance Report*\n\n"
        "Revenue / Expense / Profit Analysis Ready ✅",
        parse_mode="Markdown"
    )
