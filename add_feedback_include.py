from pathlib import Path

p = Path("src/main.py")

s = p.read_text()

old = '''app.include_router(ui_dashboard_router)
'''

new = '''app.include_router(ui_dashboard_router)
app.include_router(feedback_router)
'''

if old in s:
    s = s.replace(old,new,1)
    p.write_text(s)
    print("✅ feedback router included")
else:
    print("❌ include location not found")
