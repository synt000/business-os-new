from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from src.core.database import get_db
from src.models.saas_core import Customer


NAME, PHONE, EMAIL = range(3)


async def start_customer_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "➕ Customer Name:"
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["customer_name"] = update.message.text

    await update.message.reply_text(
        "📞 Phone Number:"
    )

    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        "📧 Email:"
    )

    return EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["email"] = update.message.text

    db = next(get_db())

    try:
        customer = Customer(
            customer_name=context.user_data["customer_name"],
            customer_phone=context.user_data["phone"],
            customer_email=context.user_data["email"],
            tenant_id="default"
        )

        db.add(customer)
        db.commit()

        await update.message.reply_text(
            "✅ Customer Created Successfully"
        )

    except Exception as e:
        db.rollback()

        await update.message.reply_text(
            f"❌ Error: {e}"
        )

    finally:
        db.close()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ Cancelled"
    )

    return ConversationHandler.END


def customer_add_conversation():

    return ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^➕ Add Customer$"),
                start_customer_add
            )
        ],

        states={
            NAME:[
                MessageHandler(
                    filters.TEXT,
                    get_name
                )
            ],

            PHONE:[
                MessageHandler(
                    filters.TEXT,
                    get_phone
                )
            ],

            EMAIL:[
                MessageHandler(
                    filters.TEXT,
                    get_email
                )
            ],
        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel
            )
        ]
    )
