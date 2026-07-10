from pathlib import Path

p = Path("src/static/app.js")
text = p.read_text()

old = '''localStorage.setItem("access_token",d.access_token);
        location="/dashboard";'''

new = '''localStorage.setItem("access_token", d.access_token);

        if (d.workspace_id) {
            localStorage.setItem("tenant_id", d.workspace_id);
        }

        if (d.role_profile) {
            localStorage.setItem("role_profile", d.role_profile);
        }

        location="/dashboard";'''

if old in text:
    text = text.replace(old, new)
    p.write_text(text)
    print("LOGIN STORAGE PATCHED")
else:
    print("TARGET BLOCK NOT FOUND")
