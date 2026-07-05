from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()

app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

# Database Setup
def init_db():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("apps/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/start")
async def start_os(os_name: str = Form(...)):
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (os_name,))
    conn.commit()
    conn.close()
    return {"message": f"Welcome {os_name}, မင်းရဲ့ နာမည်ကို Database ထဲမှာ သိမ်းလိုက်ပြီ!"}
