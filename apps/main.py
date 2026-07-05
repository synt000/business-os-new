from fastapi import FastAPI, Form
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

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()
    conn.close()
    user_list = "".join([f"<li>{u[0]}</li>" for u in users])
    return f"<html><body><h1>User Dashboard</h1><ul>{user_list}</ul><a href='/'>Back</a></body></html>"

@app.post("/start")
async def start_os(os_name: str = Form(...)):
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (os_name,))
    conn.commit()
    conn.close()
    return {"message": f"Welcome {os_name}, နာမည်ကို သိမ်းပြီးပြီ! <a href='/dashboard'>Dashboard သို့သွားရန်</a>"}
