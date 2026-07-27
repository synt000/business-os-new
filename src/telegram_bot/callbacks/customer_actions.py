from telegram import Update
from telegram.ext import ContextTypes
from src.core.database import get_db
from src.models.saas_core import Customer


async def customer_list_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    print('🔥 CUSTOMER LIST CALLBACK START')
    await query.answer()

    db = next(get_db())

    try:
        customers = db.query(Customer).limit(10).all()

        if not customers:
            text = (
                "👥 *Customer List*\n\n"
                "No customers found."
            )
        else:
            text = "👥 *Customer List*\n\n"

            for c in customers:
                text += (
                    f"• {c.customer_name}\n"
                    f"  📞 {c.customer_phone or '-'}\n\n"
                )

    finally:
        db.close()

    await query.message.reply_text(
        text,
        parse_mode="Markdown"
    )


async def customer_add_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    print('🔥 CUSTOMER ADD CALLBACK START')
    await query.answer()

    await query.message.reply_text(
        "➕ *Add Customer*\n\n"
        "Customer Creation Engine Ready ✅",
        parse_mode="Markdown"
    )


async def customer_analysis_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    print('🔥 CUSTOMER ANALYSIS CALLBACK START')
    await query.answer()

    db = next(get_db())

    try:
        total = db.query(Customer).count()

    finally:
        db.close()

    await query.message.reply_text(
        "📊 *Customer Analysis*\n\n"
        f"👥 Total Customers: {total}\n"
        "Analytics Engine Ready ✅",
        parse_mode="Markdown"
    )
