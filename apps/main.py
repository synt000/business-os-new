# (အပေါ်ပိုင်း ကုဒ်တွေ အတိုင်းပဲထားပြီး dashboard function ကို ဒီလိုပြင်လိုက်ပါ)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    conn = sqlite3.connect("business_os.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()
    conn.close()
    
    rows = "".join([f"<tr><td>{u[0]}</td></tr>" for u in users])
    return f"""
    <html>
    <head><link rel='stylesheet' href='/static/style.css'></head>
    <body class='dark-mode'>
        <div class='main-content'>
            <h1>User Dashboard</h1>
            <table><tr><th>Registered Users</th></tr>{rows}</table>
            <br><a href='/'>Back Home</a>
        </div>
    </body>
    </html>
    """
