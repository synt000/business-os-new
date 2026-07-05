from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import csv
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

ADMIN_PASSWORD = "123"  # မင်း ကြိုက်တဲ့ Password ပြောင်းလို့ရတယ်

def init_db():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """<html><body>
    <h1>Login to Business OS</h1>
    <form action='/login' method='post'>
        <input type='password' name='password' placeholder='Enter Password' required>
        <button type='submit'>Login</button>
    </form>
    </body></html>"""

@app.post("/login")
async def login(password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        return RedirectResponse(url="/dashboard", status_code=303)
    return "<h1>Wrong Password!</h1><a href='/'>Try Again</a>"

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    # ဒီနေရာမှာ Security အတွက် တကယ်တော့ Session သုံးရမယ်၊ အခုတော့ အလွယ်နည်းနဲ့
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM todos")
    todos = cursor.fetchall()
    conn.close()
    rows = "".join([f"<tr><td>{t[1]}</td><td><a href='/delete-todo/{t[0]}'>Delete</a></td></tr>" for t in todos])
    return f"<html><body><h1>Dashboard</h1><a href='/export'>Download CSV</a><table>{rows}</table><a href='/'>Logout</a></body></html>"

@app.post("/add-todo")
async def add_todo(task: str = Form(...)):
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/delete-todo/{todo_id}")
async def delete_todo(todo_id: int):
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/export")
async def export_data():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM todos")
    data = cursor.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Task"])
    writer.writerows(data)
    output.seek(0)
    return StreamingResponse(io.BytesIO(output.getvalue().encode()), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=tasks.csv"})
