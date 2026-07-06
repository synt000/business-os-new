from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import os

app = FastAPI()

# Database path ကို /tmp သို့မဟုတ် persistent storage ရှိမည့်နေရာသို့ သတ်မှတ်ခြင်း
DB_PATH = "business_os.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Application startup မှာ DB စစ်ဆေးခြင်း
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def login():
    return "<html><body><h1>Business OS</h1><a href='/dashboard'>Login to Dashboard</a></body></html>"

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(search: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        if search:
            cursor.execute("SELECT id, task FROM todos WHERE task LIKE ?", ('%' + search + '%',))
        else:
            cursor.execute("SELECT id, task FROM todos")
        todos = cursor.fetchall()
    except sqlite3.OperationalError:
        todos = []
    conn.close()

    rows = "".join([f"<tr><td>{t[1]}</td><td><a href='/delete-todo/{t[0]}'>Delete</a></td></tr>" for t in todos])
    return f"""<html><head><link rel='stylesheet' href='/static/style.css'></head>
               <body><div class='container'>
               <h1>Business OS Dashboard</h1>
               <form action='/dashboard' method='get'><input type='text' name='search' placeholder='Search tasks...'><button type='submit'>Search</button></form>
               <table><tr><th>Task</th><th>Action</th></tr>{rows}</table>
               <br><a href='/'>Logout</a>
               </div></body></html>"""
