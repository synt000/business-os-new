from telegram import Update
from telegram.ext import ContextTypes
from src.telegram_bot.keyboards import dashboard_menu

from dotenv import load_dotenv
import requests
import os

load_dotenv(".env")


async def dashboard_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    try:
        email = os.getenv("CEO_EMAIL")
        password = os.getenv("CEO_PASSWORD")

        login = requests.post(
            "http://127.0.0.1:8000/api/v4/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=15
        )

        login.raise_for_status()

        token = login.json()["access_token"]

        res = requests.get(
            "http://127.0.0.1:8000/api/v4/dashboard/summary",
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=15
        )

        res.raise_for_status()

        data = res.json()

        text = (
            "📊 *Dashboard*\n\n"
            f"📦 Products: {data.get('products',0)}\n"
            f"🧾 Orders: {data.get('orders',0)}\n"
            f"👥 Customers: {data.get('customers',0)}\n"
            f"🏭 Suppliers: {data.get('suppliers',0)}\n\n"
            f"💰 Revenue: ${data.get('revenue',0)}\n"
            f"💸 Expense: ${data.get('expense',0)}\n"
            f"📈 Profit: ${data.get('profit',0)}"
        )

    except Exception as e:
        text = (
            "📊 Dashboard\n\n"
            f"❌ API Error: {e}"
        )

    await query.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=dashboard_menu()
    )
