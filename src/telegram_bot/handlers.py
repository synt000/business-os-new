from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
🤖 Business OS CEO Bot Online

Welcome Bro.

📊 Dashboard
💰 Finance
📦 Inventory
👥 Customers

System Connected Successfully.
        """
    )


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📊 Dashboard\n\nSales: Loading...\nOrders: Loading...\nRevenue: Loading..."
    )


async def finance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💰 Finance Module\n\nCashflow: Connected\nInvoices: Connected"
    )


async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📦 Inventory Module\n\nStock Engine Connected"
    )


async def customers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👥 Customer CRM Connected"
    )
