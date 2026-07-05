from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

# Database ပြင်ဆင်ခြင်း
def init_db():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT)")
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
    return HTMLResponse("<h1>Task Added!</h1><a href='/dashboard'>Back to Dashboard</a>")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task FROM todos")
    todos = cursor.fetchall()
    conn.close()
    rows = "".join([f"<tr><td>{t[0]}</td></tr>" for t in todos])
    return f"""<html><head><link rel='stylesheet' href='/static/style.css'></head>
    <body class='dark-mode'>
        <div class='main-content'>
            <h1>To-Do List Dashboard</h1>
            <div class='card'>
                <form action='/add-todo' method='post'>
                    <input type='text' name='task' placeholder='New Task...' required>
                    <button type='submit'>Add Task</button>
                </form>
            </div>
            <table><tr><th>My Tasks</th></tr>{rows}</table>
            <br><a href='/'>Back Home</a>
        </div>
    </body></html>"""

@app.post("/start")
async def start_os(os_name: str = Form(...)):
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (os_name,))
    conn.commit()
    conn.close()
    return {"message": f"Welcome {os_name}! <a href='/dashboard'>Go to Dashboard</a>"}
