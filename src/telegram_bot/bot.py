import os
import asyncio
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

load_dotenv(".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Business OS CEO\n\n"
        "Bot is running successfully."
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Business OS Server Alive")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    print("🤖 Business OS CEO Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    main()
