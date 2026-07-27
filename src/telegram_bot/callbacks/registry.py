from telegram.ext import CallbackQueryHandler

from .dashboard import dashboard_callback
from .finance import finance_callback
from .inventory import inventory_callback
from .customer import customer_callback
from .supplier import supplier_callback
from .settings import settings_callback
from .users import users_callback
from .security import security_callback


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

    elif data == "inventory":
        await inventory_callback(
            update,
            context
        )

    elif data == "settings":
        await settings_callback(
            update,
            context
        )

    elif data == "manage_users":
        await users_callback(
            update,
            context
        )

    elif data == "security_center":
        await security_callback(
            update,
            context
        )

    elif data == "customer":
        await customer_callback(update, context)

    elif data == "supplier":
        await supplier_callback(update, context)

    else:
        await query.message.reply_text(
            f"Callback: {data}"
        )
