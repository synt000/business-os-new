from telegram.ext import CommandHandler

from .start import start_handler
from .dashboard import dashboard_handler
from .finance import finance_handler
from .inventory import inventory_handler
from .customer import customer_handler
from .report import report_handler
from .supplier import supplier_handler


def register_handlers(app):

    app.add_handler(
        CommandHandler("start", start_handler)
    )

    app.add_handler(
        CommandHandler("dashboard", dashboard_handler)
    )

    app.add_handler(
        CommandHandler("finance", finance_handler)
    )

    app.add_handler(
        CommandHandler("inventory", inventory_handler)
    )

    app.add_handler(
        CommandHandler("customer", customer_handler)
    )

    app.add_handler(
        CommandHandler("report", report_handler)
    )

    app.add_handler(
        CommandHandler("supplier", supplier_handler)
    )
