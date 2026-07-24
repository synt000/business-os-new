from pathlib import Path

p = Path("src/static/js/dashboard_api.js")

s = p.read_text()

old = '''if(errorBox){
        errorBox.innerText =
        "⚠️ Dashboard temporarily unavailable. Please try again.";
    }'''

new = '''if(errorBox){

        errorBox.style.display = "block";

        errorBox.innerText =
        "⚠️ Dashboard temporarily unavailable. Please try again.";

    }'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ error banner display enabled")
else:
    print("❌ target not found")
