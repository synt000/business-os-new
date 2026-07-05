from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

def init_db():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("apps/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

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

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM todos")
    todos = cursor.fetchall()
    conn.close()
    rows = "".join([f"<tr><td>{t[1]}</td><td><a href='/delete-todo/{t[0]}' style='color:red;'>Delete</a></td></tr>" for t in todos])
    return f"""<html><head><link rel='stylesheet' href='/static/style.css'></head>
    <body class='dark-mode'>
        <div class='main-content'>
            <h1>To-Do Dashboard</h1>
            <div class='card'>
                <form action='/add-todo' method='post'>
                    <input type='text' name='task' placeholder='New Task...' required>
                    <button type='submit'>Add Task</button>
                </form>
            </div>
            <table><tr><th>Task</th><th>Action</th></tr>{rows}</table>
            <br><a href='/'>Back Home</a>
        </div>
    </body></html>"""
