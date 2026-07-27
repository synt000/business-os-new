from telegram.ext import CallbackQueryHandler

from .dashboard import dashboard_callback
from .finance import finance_callback


def register_callbacks(app):

    app.add_handler(
        CallbackQueryHandler(
            callback_router
        )
    )


async def callback_router(update, context):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "dashboard":
        await dashboard_callback(
            update,
            context
        )

    elif data == "finance":
        await finance_callback(
            update,
            context
        )

    else:
        await query.message.reply_text(
            f"Callback: {data}"
        )
