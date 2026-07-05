from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Business OS")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("apps/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()
