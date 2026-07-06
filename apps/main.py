from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI(title="Business OS API", version="1.0.0")
app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

@app.on_event("startup")
async def startup():
    conn = sqlite3.connect("business_os.db")
    conn.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL)")
    conn.close()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<html><body><h1>Business OS</h1><p>Visit <a href='/docs'>/docs</a> for API documentation.</p></body></html>"

@app.get("/dashboard")
async def dashboard():
    return {"message": "Dashboard operational"}
