from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# CSS ဖိုင်တွေကို Static အနေနဲ့ သတ်မှတ်မယ်
app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("apps/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()
