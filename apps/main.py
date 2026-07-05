from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

# ဒီနေရာမှာ app ကို အရင် Define လုပ်ရမယ်
app = FastAPI()

# Static files mount လုပ်မယ်
app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

def init_db():
    try:
        conn = sqlite3.connect("business_os.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

init_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("apps/templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "<h1>Oops! Something went wrong.</h1>"

@app.post("/start")
async def start_os(os_name: str = Form(...)):
    if not os_name or len(os_name.strip()) == 0:
        raise HTTPException(status_code=400, detail="နာမည်ထည့်ဖို့ လိုအပ်ပါတယ်!")
    try:
        conn = sqlite3.connect("business_os.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (os_name.strip(),))
        conn.commit()
        conn.close()
        return {"message": f"Welcome {os_name.strip()}, နာမည်ကို အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ! <a href='/dashboard'>Dashboard သို့</a>"}
    except Exception:
        raise HTTPException(status_code=500, detail="Database error occurred.")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    try:
        conn = sqlite3.connect("business_os.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users")
        users = cursor.fetchall()
        conn.close()
        rows = "".join([f"<tr><td>{u[0]}</td></tr>" for u in users])
        return f"<html><head><link rel='stylesheet' href='/static/style.css'></head><body class='dark-mode'><div class='main-content'><h1>Dashboard</h1><table><tr><th>Registered Users</th></tr>{rows}</table><br><a href='/'>Back Home</a></div></body></html>"
    except Exception:
        return "<h1>Error loading dashboard.</h1>"
