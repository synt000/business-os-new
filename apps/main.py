from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

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
    # Input Validation: နာမည်က အလွတ်ဖြစ်နေရင် တားဆီးမယ်
    if not os_name or len(os_name.strip()) == 0:
        raise HTTPException(status_code=400, detail="နာမည်ထည့်ဖို့ လိုအပ်ပါတယ်!")
    
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    # Sanitization: User input ကို သန့်စင်ပြီးမှ သိမ်းမယ်
    cursor.execute("INSERT INTO users (name) VALUES (?)", (os_name.strip(),))
    conn.commit()
    conn.close()
    return {"message": f"Welcome {os_name.strip()}, နာမည်ကို အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ! <a href='/dashboard'>Dashboard သို့</a>"}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()
    conn.close()
    user_list = "".join([f"<li>{u[0]}</li>" for u in users])
    return f"<html><body><h1>Dashboard</h1><ul>{user_list}</ul><a href='/'>Back</a></body></html>"
