from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

old = """🚀 Premium Dashboard"""

new = """
<div class="theme-toggle-wrap">
    <button id="themeToggle" class="theme-toggle">
        🌙 Dark
    </button>
</div>

🚀 Premium Dashboard
"""

if old not in s:
    print("target not found")
else:
    s = s.replace(old, new, 1)
    p.write_text(s)
    print("theme toggle button added")
