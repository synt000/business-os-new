from pathlib import Path

p = Path("src/telegram_bot/webhook.py")
text = p.read_text()

old = '''async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🚀 START COMMAND RECEIVED")

    await update.message.reply_text(
        "🤖 Business OS CEO Bot Online\\n\\n"
        "Welcome Bro.\\n\\n"
        "Choose Module:",
        reply_markup=ceo_main_menu()
    )
'''

new = '''import requests

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🚀 START COMMAND RECEIVED")

    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": update.effective_chat.id,
            "text": "✅ Webhook OK\\nDirect sendMessage success."
        },
        timeout=15,
    )

    print("SEND:", r.status_code)
    print(r.text)
'''

if old not in text:
    raise SystemExit("start block not found")

p.write_text(text.replace(old, new))
print("✅ patched")
