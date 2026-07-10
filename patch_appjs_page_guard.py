from pathlib import Path

p = Path("src/static/app.js")
text = p.read_text()

old = """window.onload=loadDashboard;"""

new = """window.onload=function(){
    if(window.location.pathname === "/dashboard"){
        loadDashboard();
    }
};"""

if old in text:
    text = text.replace(old,new)
    p.write_text(text)
    print("APP.JS PAGE GUARD PATCHED")
else:
    print("TARGET NOT FOUND")
