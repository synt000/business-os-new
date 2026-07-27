from telegram.ext import CallbackQueryHandler

from .dashboard import dashboard_callback
from .finance import finance_callback
from .inventory import inventory_callback
from .customer import customer_callback
from .supplier import supplier_callback
from .report import report_callback
from .report_actions import (
    sales_report_callback,
    inventory_report_callback,
    finance_report_callback
)
from .settings import settings_callback
from .users import users_callback
from .security import security_callback


def register_callbacks(app):

    app.add_handler(
        CallbackQueryHandler(callback_router)
    )


async def callback_router(update, context):

    query = update.callback_query
    data = query.data

    try:
        await query.answer(cache_time=1)
    except Exception:
        pass

    if data == "dashboard":
        await dashboard_callback(update, context)

    elif data == "finance":
        await finance_callback(update, context)

    elif data == "inventory":
        await inventory_callback(update, context)

    elif data == "settings":
        await settings_callback(update, context)

    elif data == "manage_users":
        await users_callback(update, context)

    elif data == "security_center":
        await security_callback(update, context)

    elif data == "customer":
        await customer_callback(update, context)

    elif data == "supplier":
        await supplier_callback(update, context)

    elif data == "report":
        await report_callback(update, context)

    elif data == "sales_report":
        await sales_report_callback(update, context)

    elif data == "inventory_report":
        await inventory_report_callback(update, context)

    elif data == "finance_report":
        await finance_report_callback(update, context)

    else:
        await query.message.reply_text(
            f"Callback: {data}"
        )
