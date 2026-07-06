from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import sqlite3, csv, io

app = FastAPI()
app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

ADMIN_PASSWORD = "123"

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(search: str = ""):
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    if search:
        cursor.execute("SELECT id, task FROM todos WHERE task LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT id, task FROM todos")
    todos = cursor.fetchall()
    conn.close()
    
    rows = "".join([f"<tr><td>{t[1]}</td><td><a href='/delete-todo/{t[0]}' class='delete-btn'>Delete</a></td></tr>" for t in todos])
    
    return f"""<html><head><link rel='stylesheet' href='/static/style.css'></head>
    <body><div class='container'>
    <h1>Business OS Dashboard</h1>
    <form action='/dashboard' method='get'><input type='text' name='search' placeholder='Search tasks...'><button type='submit'>Search</button></form>
    <table><tr><th>Task</th><th>Action</th></tr>{rows}</table>
    <a href='/export' class='export-link'>Download Data (CSV)</a>
    <br><a href='/' style='color:#888;'>Logout</a>
    </div></body></html>"""
