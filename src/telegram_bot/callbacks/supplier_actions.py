from telegram import Update
from telegram.ext import ContextTypes

from src.core.database import get_db
from src.models.saas_core import Supplier


async def supplier_list_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    db = next(get_db())

    try:
        suppliers = db.query(Supplier).limit(10).all()

        if not suppliers:
            text = (
                "🏭 *Supplier List*\n\n"
                "No suppliers found."
            )
        else:
            text = "🏭 *Supplier List*\n\n"

            for s in suppliers:
                text += (
                    f"• {s.supplier_name}\n"
                    f"  📞 {s.contact_phone or 'N/A'}\n"
                    f"  💰 Balance: {s.current_balance}\n\n"
                )

        await query.message.reply_text(
            text,
            parse_mode="Markdown"
        )

    finally:
        db.close()


async def supplier_add_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "➕ *Add Supplier*\n\n"
        "Supplier Creation Engine Ready ✅",
        parse_mode="Markdown"
    )


async def supplier_analysis_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    db = next(get_db())

    try:
        count = db.query(Supplier).count()

        text = (
            "📈 *Supplier Analysis*\n\n"
            f"🏭 Total Suppliers: {count}\n"
            "Analytics Engine Ready ✅"
        )

        await query.message.reply_text(
            text,
            parse_mode="Markdown"
        )

    finally:
        db.close()
