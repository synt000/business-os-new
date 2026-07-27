from telegram.ext import CommandHandler

from .start import start_handler
from .dashboard import dashboard_handler


def register_handlers(app):

    app.add_handler(
        CommandHandler("start", start_handler)
    )

    app.add_handler(
        CommandHandler("dashboard", dashboard_handler)
    )
