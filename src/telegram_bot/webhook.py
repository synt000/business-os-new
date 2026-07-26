from fastapi import APIRouter, Request
from telegram import Update
from telegram.ext import Application, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv(".env")

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram Bot"]
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

telegram_app = Application.builder().token(TOKEN).build()


async def start_command(update: Update, context):
    print("🔥 START COMMAND RECEIVED")

    if update.message:
        await update.message.reply_text(
            "🤖 Business OS CEO Bot Online\n\n"
            "Welcome Bro.\n"
            "System is connected successfully."
        )


telegram_app.add_handler(
    CommandHandler("start", start_command)
)


@router.on_event("startup")
async def telegram_startup():
    print("🤖 Telegram CEO Bot Initialized")


@router.on_event("shutdown")
async def telegram_shutdown():
    print("🛑 Telegram CEO Bot Shutdown")


@router.post("/webhook")
async def telegram_webhook(request: Request):

    if not telegram_app.bot._initialized:
        await telegram_app.initialize()

    data = await request.json()

    print("🔥 RAW TELEGRAM DATA:", data)

    update = Update.de_json(
        data,
        telegram_app.bot
    )

    print("🔥 TELEGRAM UPDATE:", update)

    await telegram_app.process_update(update)

    return {
        "status": "ok"
    }
