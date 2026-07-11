from pathlib import Path

p = Path("src/core/middlewares.py")
t = p.read_text()

old = 'response.headers["Content-Security-Policy"] = "default-src \'self\';\'unsafe-inline\'https:;frame-ancestors \'none\';"'

new = '''response.headers["Content-Security-Policy"] = (
    "default-src 'self' https:; "
    "script-src 'self' 'unsafe-inline' https:; "
    "style-src 'self' 'unsafe-inline' https:; "
    "font-src 'self' https: data:; "
    "img-src 'self' data: https:; "
    "frame-ancestors 'none';"
)'''

if old in t:
    t = t.replace(old, new)
    p.write_text(t)
    print("CSP FIXED")
else:
    print("TARGET NOT FOUND")
