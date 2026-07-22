from pathlib import Path

p = Path("src/static/css/owner_dashboard.css")

s = p.read_text()

css = """

/* BUSINESS OS THEME TOGGLE */

.theme-toggle-wrap{
    display:flex;
    justify-content:flex-end;
    margin-bottom:12px;
}

.theme-toggle{
    background:#1e1e2e;
    color:#ffffff;
    border:1px solid #3b82f6;
    padding:8px 14px;
    border-radius:12px;
    cursor:pointer;
    font-size:14px;
}

.theme-toggle:hover{
    background:#2563eb;
}

body.light-theme{
    background:#f5f7fb;
    color:#111827;
}

body.light-theme .dashboard-card{
    background:#ffffff;
    color:#111827;
}

"""

if "BUSINESS OS THEME TOGGLE" not in s:
    s += css
    p.write_text(s)
    print("theme toggle css added")
else:
    print("already exists")
