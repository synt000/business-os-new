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
from .inventory_actions import inventory_stock_callback, inventory_movements_callback, inventory_warehouse_callback

from .finance_actions import finance_revenue_callback, finance_expense_callback, finance_profit_callback

from .users_center import users_list_callback, rbac_roles_callback, permissions_callback


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

    elif data == "finance_revenue":
        await finance_revenue_callback(update, context)

    elif data == "finance_expense":
        await finance_expense_callback(update, context)

    elif data == "finance_profit":
        await finance_profit_callback(update, context)

    elif data == "inventory":
        await inventory_callback(update, context)

    elif data == "inventory_stock":
        await inventory_stock_callback(update, context)

    elif data == "inventory_movements":
        await inventory_movements_callback(update, context)

    elif data == "inventory_warehouse":
        await inventory_warehouse_callback(update, context)

    elif data == "settings":
        await settings_callback(update, context)

    elif data == "manage_users":
        await users_callback(update, context)

    elif data == "security_center":
        await security_callback(update, context)


    elif data == "users_list":
        await users_list_callback(update, context)

    elif data == "rbac_roles":
        await rbac_roles_callback(update, context)

    elif data == "permissions":
        await permissions_callback(update, context)

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

