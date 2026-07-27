import os
import asyncio

from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler
)

from src.telegram_bot.handlers.start import start_command


load_dotenv(".env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def main():

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )


    print("🤖 Telegram CEO Bot Polling Started")


    await app.initialize()
    await app.start()
    await app.updater.start_polling()


    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
