from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

marker = "/* AI PROCUREMENT PANEL */"

css = '''
/* FEEDBACK CENTER */

.feedback-section{
    margin-top:20px;
}

.feedback-card{
    background:#111827;
    border-radius:18px;
    padding:16px;
    border:1px solid #1f2937;
}

.feedback-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
    margin-top:15px;
}

.feedback-btn{
    background:#0f172a;
    border:1px solid #334155;
    padding:14px;
    border-radius:14px;
    color:white;
    text-align:center;
    cursor:pointer;
    transition:.2s;
}

.feedback-btn:hover{
    transform:translateY(-3px);
    border-color:#00e5ff;
}

.feedback-icon{
    font-size:24px;
    margin-bottom:8px;
}

.feedback-text{
    font-size:13px;
}

'''

if "FEEDBACK CENTER" not in s:
    s=s.replace(marker, css + marker, 1)
    p.write_text(s)
    print("✅ feedback CSS added")
else:
    print("⚠️ already exists")
