from telegram import Update
from telegram.ext import ContextTypes


async def inventory_stock_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📦 *Stock Overview*\n\n"
        "Inventory Stock Data Ready ✅",
        parse_mode="Markdown"
    )


async def inventory_movements_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "🔄 *Stock Movements*\n\n"
        "Movement Tracking Ready ✅",
        parse_mode="Markdown"
    )


async def inventory_warehouse_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "🏭 *Warehouse Analysis*\n\n"
        "Warehouse Overview Ready ✅",
        parse_mode="Markdown"
    )
