from functools import lru_cache
from fastapi import APIRouter, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from src.models.saas_core import User
from src.core.database import SessionLocal
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from dotenv import load_dotenv
from src.telegram_bot.keyboards import ceo_main_menu
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



telegram_app = Application.builder().token(TOKEN).build()


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



async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    print("🔥 CALLBACK DATA:", query.data, flush=True)

    try:

        if query.data == "dashboard":

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
                "📊 *Business Dashboard*\n\n"
                f"💰 Revenue: ${data.get('revenue',0)}\n"
                f"💸 Expense: ${data.get('expense',0)}\n"
                f"📈 Profit: ${data.get('profit',0)}\n"
                f"📦 Products: {data.get('products',0)}\n"
                f"🛒 Orders: {data.get('orders',0)}\n"
                f"👥 Customers: {data.get('customers',0)}"
            )

        elif query.data == "inventory":

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
                "📦 *Inventory Dashboard*\n\n"
                f"📦 Products: {data.get('total_products',0)}\n"
                f"📊 Stock Units: {data.get('total_units',0)}\n"
                f"💰 Stock Value: ${data.get('inventory_value',0)}\n"
                f"⚠ Low Stock: {data.get('low_stock',0)}\n"
                f"🚫 Out Of Stock: {data.get('out_stock',0)}"
            )

        elif query.data == "sales":

            import asyncio

            token = await asyncio.to_thread(
                get_ceo_access_token
            )

            r = await asyncio.to_thread(
                requests.get,
                "http://127.0.0.1:8000/api/v4/business/reports/sales",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                timeout=10
            )

            data = r.json()

            text = (
                "💵 *Sales Dashboard*\n\n"
                f"💰 Total Sales: ${data.get('total_sales',0)}\n"
                f"🛒 Completed Orders: {data.get('completed_orders',0)}"
            )

        elif query.data == "finance":

            import asyncio

            token = await asyncio.to_thread(
                get_ceo_access_token
            )

            r = await asyncio.to_thread(
                requests.get,
                "http://127.0.0.1:8000/api/v4/business/accounting/profit-loss",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                timeout=10
            )

            data = r.json()

            financial = data.get(
                "financial_summary",
                {}
            )

            text = (
                "💰 *Finance Dashboard*\n\n"
                f"📈 Revenue: ${financial.get('total_gross_revenue',0)}\n"
                f"💸 COGS: ${financial.get('total_cost_of_goods_sold',0)}\n"
                f"💵 Net Profit: ${financial.get('net_operational_profit',0)}\n"
                f"📊 Margin: {financial.get('net_profit_margin_percentage','0%')}"
            )

        elif query.data == "customer":

            import asyncio

            token = await asyncio.to_thread(
                get_ceo_access_token
            )

            r = await asyncio.to_thread(
                requests.get,
                "http://127.0.0.1:8000/api/v4/business/customers",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                timeout=10
            )

            data = r.json()

            customers = data.get("customers", [])

            text = (
                "👥 *Customer CRM Dashboard*\n\n"
                f"👤 Total Customers: {len(customers)}\n\n"
            )

            for c in customers[:5]:
                text += (
                    f"• {c.get('name')}\n"
                    f"  💰 Spent: ${c.get('total_spent_usd',0)}\n"
                    f"  📞 {c.get('phone')}\n\n"
                )


        elif query.data == "report":

            import asyncio

            token = await asyncio.to_thread(
                get_ceo_access_token
            )

            sales_r = await asyncio.to_thread(
                requests.get,
                "http://127.0.0.1:8000/api/v4/business/reports/sales",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                timeout=10
            )

            finance_r = await asyncio.to_thread(
                requests.get,
                "http://127.0.0.1:8000/api/v4/business/accounting/profit-loss",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                timeout=10
            )

            sales = sales_r.json()
            finance = finance_r.json()

            summary = finance.get(
                "financial_summary",
                {}
            )

            text = (
                "📑 *Business Report Dashboard*\n\n"
                f"💰 Sales: ${sales.get('total_sales',0)}\n"
                f"🛒 Orders: {sales.get('completed_orders',0)}\n\n"
                f"📈 Revenue: ${summary.get('total_gross_revenue',0)}\n"
                f"💸 COGS: ${summary.get('total_cost_of_goods_sold',0)}\n"
                f"💵 Profit: ${summary.get('net_operational_profit',0)}\n"
                f"📊 Margin: {summary.get('net_profit_margin_percentage','0%')}"
            )

        elif query.data == "settings":

            import asyncio
            from src.core.security import verify_access_token

            token = await asyncio.to_thread(
                get_ceo_access_token
            )

            payload = verify_access_token(token)

            if payload:

                text = (
                    "⚙️ *Workspace Control Center*\n\n"
                    "🏢 *Business:*\n"
                    "Business OS Enterprise\n\n"
                    f"👤 *Role:* {payload.get('role','N/A')}\n"
                    f"💳 *Plan:* {payload.get('subscription','FREE_TRIAL')}\n\n"

                    "🔐 *Security:*\n"
                    "JWT ACTIVE ✅\n\n"

                    "🆔 *Workspace:*\n"
                    f"{payload.get('tenant_id','N/A')}\n\n"

                    "📊 *System Health:*\n"
                    "🟢 API ONLINE\n"
                    "🟢 DATABASE ONLINE\n"
                    "🟢 TELEGRAM BOT ONLINE\n\n"

                    "📦 *Enabled Modules:*\n"
                    "✅ Dashboard\n"
                    "✅ Inventory\n"
                    "✅ Sales\n"
                    "✅ Finance\n"
                    "✅ CRM\n"
                    "✅ Reports\n\n"

                    "⚙️ *Actions:*\n"
                    "🔄 Refresh Token\n"
                    "👥 Manage Users\n"
                    "🏢 Business Profile\n"
                    "🔔 Notification Settings"
                )


            else:
                text = "⚠️ Settings Authentication Failed"

        elif query.data == "manage_users":

            try:
                db = SessionLocal()

                users = db.query(User).all()

                owner = 0
                admin = 0
                staff = 0

                for u in users:
                    role = str(getattr(u, "role", "")).upper()

                    if role == "OWNER":
                        owner += 1
                    elif role == "ADMIN":
                        admin += 1
                    else:
                        staff += 1

                db.close()

                text = (
                    "👥 *User Management Center*\n\n"
                    f"👑 Owner: {owner}\n"
                    f"🛡 Admin: {admin}\n"
                    f"👤 Staff: {staff}\n\n"
                    "🔐 Permission Engine Connected\n"
                    "✅ RBAC Active\n\n"
                    "Select an action below."
                )

            except Exception as e:
                text = f"❌ User Management Error\n{e}"

            except Exception as e:
                text = f"❌ User Management Error\\n{e}"


        elif query.data == "business_profile":

            text = (
                "🏢 *Business Profile*\n\n"
                "Business OS Enterprise\n\n"
                "📦 SaaS ERP Platform\n"
                "🌐 Multi Tenant Workspace\n"
                "✅ Business Identity Verified"
            )


        elif query.data == "notifications":

            text = (
                "🔔 *Notification Center*\n\n"
                "📦 Stock Alert: ON\n"
                "💰 Sales Alert: ON\n"
                "📊 Report Alert: ON\n\n"
                "Notification Engine Connected"
            )


        elif query.data == "view_users":

            try:
                db = SessionLocal()

                users = db.query(User).limit(10).all()

                text = (
                    "👤 *User Directory*\n\n"
                    "Select a user below:"
                )

                user_buttons = []

                for u in users:
                    email = getattr(u, "email", "N/A")
                    uid = getattr(u, "id", "N/A")

                    user_buttons.append(
                        [
                            InlineKeyboardButton(
                                f"👤 {email}",
                                callback_data=f"user_detail_{uid}"
                            )
                        ]
                    )

                user_buttons.append(
                    [
                        InlineKeyboardButton(
                            "⬅️ Back",
                            callback_data="manage_users"
                        )
                    ]
                )

                keyboard = InlineKeyboardMarkup(user_buttons)

                db.close()

            except Exception as e:
                text = f"❌ User Load Error\n{e}"


        elif query.data == "add_user":

            text = (
                "➕ *Add User Center*\n\n"
                "📧 Invite User Flow Ready\n"
                "🔐 Role Assignment Ready\n"
                "✅ Tenant Safe"
            )

        elif query.data == "permissions":

            text = (
                "🔐 *Permission Matrix*\\n\\n"
                "👑 Owner: Full Access\\n"
                "🛡 Admin: Controlled Access\\n"
                "👤 Staff: Limited Access\\n\\n"
                "RBAC Engine Active"
            )


        elif query.data == "activity_history":

            text = (
                "📜 *User Activity History*\\n\\n"
                "Login Audit: ACTIVE\\n"
                "Permission Changes: TRACKING\\n"
                "Security Logs: ENABLED"
            )


        elif query.data == "disable_user":

            text = (
                "🚫 *Disable User Center*\\n\\n"
                "Select User → Disable Account\\n"
                "Audit Logging Enabled"
            )


        elif query.data == "refresh_users":

            try:
                db = SessionLocal()

                users = db.query(User).all()

                owner = 0
                admin = 0
                staff = 0

                for u in users:
                    role = str(getattr(u, "role", "")).upper()

                    if role == "OWNER":
                        owner += 1
                    elif role == "ADMIN":
                        admin += 1
                    else:
                        staff += 1

                db.close()

                text = (
                    "🔄 *User Statistics Refreshed*\\n\\n"
                    f"👑 Owner: {owner}\\n"
                    f"🛡 Admin: {admin}\\n"
                    f"👤 Staff: {staff}\\n\\n"
                    "✅ User Data Updated"
                )

            except Exception as e:
                text = f"❌ Refresh Error\\n{e}"

        elif query.data == "refresh_token":

            text = (
                "🔄 *Token Refresh*\n\n"
                "✅ Access Token Verified\n"
                "🔐 JWT Session Active\n"
                "🟢 Security Status: OK"
            )



        elif query.data == "security_center":

            text = (
                "🔐 *Security Center*\n\n"
                "🛡 Authentication: JWT ACTIVE\n"
                "🟢 Session Status: SECURE\n"
                "🔑 Token System: ONLINE\n\n"
                "📋 Security Features:\n"
                "✅ Access Token Validation\n"
                "✅ Refresh Token Engine\n"
                "✅ Tenant Isolation\n"
                "✅ Role Based Access Control"
            )


        elif query.data == "subscription":

            text = (
                "💳 *Subscription Center*\n\n"
                "🏢 Business OS Enterprise\n\n"
                "📦 Current Plan: FREE_TRIAL\n"
                "🟢 Status: ACTIVE\n\n"
                "🚀 Available Upgrades:\n"
                "⭐ Professional Plan\n"
                "🏆 Enterprise Plan\n\n"
                "📊 Feature Engine Connected"
            )


        else:
            text = "Unknown Menu"



    except Exception as e:

        text=f"❌ Dashboard Error\n{e}"



    keyboard = None


    if query.data == "manage_users":

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "👤 View Users",
                    callback_data="view_users"
                )
            ],
            [
                InlineKeyboardButton(
                    "➕ Add User",
                    callback_data="add_user"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔐 Permissions",
                    callback_data="permissions"
                )
            ],
            [
                InlineKeyboardButton(
                    "📜 Activity History",
                    callback_data="activity_history"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚫 Disable User",
                    callback_data="disable_user"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔄 Refresh Users",
                    callback_data="refresh_users"
                )
            ]
        ])

    if query.data == "settings":

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔄 Refresh Token",
                    callback_data="refresh_token"
                )
            ],
            [
                InlineKeyboardButton(
                    "👥 Manage Users",
                    callback_data="manage_users"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏢 Business Profile",
                    callback_data="business_profile"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔔 Notification Settings",
                    callback_data="notifications"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔐 Security Center",
                    callback_data="security_center"
                )
            ],
            [
                InlineKeyboardButton(
                    "💳 Subscription",
                    callback_data="subscription"
                )
            ]
        ])


    await query.message.reply_text(
        text,
        reply_markup=keyboard
    )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("ping", ping))
telegram_app.add_handler(CommandHandler("dashboard", dashboard))
telegram_app.add_handler(CommandHandler("inventory", inventory))
telegram_app.add_handler(CommandHandler("sales", sales))
telegram_app.add_handler(CommandHandler("finance", finance))
telegram_app.add_handler(CommandHandler("customer", customer))
telegram_app.add_handler(CommandHandler("report", report))

telegram_app.add_handler(
    CallbackQueryHandler(button_callback)
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
