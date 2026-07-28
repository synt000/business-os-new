from functools import lru_cache
from fastapi import APIRouter, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from src.telegram_bot.keyboards.user_detail import user_detail_keyboard
from src.models.saas_core import User
from src.core.database import SessionLocal
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from src.telegram_bot.handlers.registry import register_handlers
from src.telegram_bot.callbacks.registry import register_callbacks
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv(".env")

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram Bot"],
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

BUSINESS_EMAIL = os.getenv("CEO_EMAIL")
BUSINESS_PASSWORD = os.getenv("CEO_PASSWORD")


@lru_cache(maxsize=1)
def get_ceo_access_token():

    r = requests.post(
        "http://127.0.0.1:8000/api/v4/auth/login",
        json={
            "email": BUSINESS_EMAIL,
            "password": BUSINESS_PASSWORD
        },
        timeout=15
    )

    r.raise_for_status()

    return r.json()["access_token"]




telegram_app = None

if TOKEN:
    telegram_app = Application.builder().token(TOKEN).build()
else:
    print("⚠️ TELEGRAM_BOT_TOKEN missing - Telegram Bot disabled")



if telegram_app:
    register_handlers(telegram_app)
    register_callbacks(telegram_app)



import requests
import os
import aiohttp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🚀 START COMMAND RECEIVED")


    keyboard = [
        [
            InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
            InlineKeyboardButton("📦 Inventory", callback_data="inventory"),
        ],
        [
            InlineKeyboardButton("💰 Sales", callback_data="sales"),
            InlineKeyboardButton("💵 Finance", callback_data="finance"),
        ],
        [
            InlineKeyboardButton("👥 Customers", callback_data="customer"),
            InlineKeyboardButton("📈 Reports", callback_data="report"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🏢 *Business OS CEO Bot*\n\n"
        "Welcome to your Business Management System.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    print("✅ START MENU SENT")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Business OS Server Alive"
    )




async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message or update.callback_query.message

    try:
        import asyncio

        token = await asyncio.to_thread(
            get_ceo_access_token
        )

        r = await asyncio.to_thread(
            requests.get,
            "http://127.0.0.1:8000/api/v4/dashboard/summary",
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=10
        )

        data = r.json()

        text = (
            "📊 *BUSINESS OS CEO REPORT*\n\n"
            "🏢 Workspace\n"
            "━━━━━━━━━━━━\n"
            f"💰 Revenue: ${data.get('revenue',0)}\n"
            f"💸 Expense: ${data.get('expense',0)}\n"
            f"📈 Profit: ${data.get('profit',0)}\n\n"

            "📦 Inventory\n"
            "━━━━━━━━━━━━\n"
            f"Products: {data.get('products',0)}\n"
            f"Low Stock: {data.get('low_stock',0)}\n\n"

            "🛒 Sales\n"
            "━━━━━━━━━━━━\n"
            f"Orders: {data.get('orders',0)}\n"
            f"Today Sales: ${data.get('today_revenue',0)}\n\n"

            "👥 CRM\n"
            "━━━━━━━━━━━━\n"
            f"Customers: {data.get('customers',0)}\n\n"

            "📈 Growth\n"
            "━━━━━━━━━━━━\n"
            f"{data.get('trends',{}).get('growth_label','')}"
        )

    except Exception as e:

        text = (
            "📊 Business Dashboard\n\n"
            "⚠ API Error\n"
            f"{e}"
        )

    await msg.reply_text(
        text,
        parse_mode="Markdown"
    )


async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message or update.callback_query.message

    try:
        import asyncio

        token = await asyncio.to_thread(
            get_ceo_access_token
        )

        r = await asyncio.to_thread(
            requests.get,
            "http://127.0.0.1:8000/api/v4/business/inventory-summary",
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=10
        )

        data = r.json()

        text = (
            "📦 Inventory Dashboard\n\n"
            f"📦 Products: {data.get('total_products',0)}\n"
            f"📊 Stock Units: {data.get('total_units',0)}\n"
            f"💰 Stock Value: ${data.get('inventory_value',0)}\n"
            f"⚠ Low Stock: {data.get('low_stock',0)}\n"
            f"🚫 Out Of Stock: {data.get('out_stock',0)}"
        )

    except Exception as e:
        text = (
            "📦 Inventory Dashboard\n\n"
            f"⚠ Error: {e}"
        )

    await msg.reply_text(text)


async def sales(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message or update.callback_query.message

    await msg.reply_text(
        "💵 Sales Report\n\nSales Engine Connected"
    )


async def finance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message or update.callback_query.message

    await msg.reply_text(
        "💰 Finance Module Connected"
    )


async def customer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message or update.callback_query.message

    await msg.reply_text(
        "👥 Customer CRM Connected"
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message or update.callback_query.message

    await msg.reply_text(
        "📑 Business Report Ready"
    )



@router.on_event("startup")
async def telegram_startup():
    try:
        await telegram_app.initialize()
        print("🤖 Telegram CEO Bot Initialized")
    except Exception as e:
        print("Telegram startup:", e)

@router.on_event("shutdown")
async def telegram_shutdown():
    try:
        await telegram_app.shutdown()
    except Exception as e:
        print("Telegram shutdown:", e)

    print("🛑 Telegram CEO Bot Shutdown")

@router.post("/webhook")
async def telegram_webhook(request: Request):

    print("📩 Telegram Update Received")

    data = await request.json()

    update = Update.de_json(
        data,
        telegram_app.bot
    )

    import asyncio

    asyncio.create_task(
        telegram_app.process_update(update)
    )

    return {
        "status": "ok"
    }
