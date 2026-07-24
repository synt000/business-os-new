from pathlib import Path

p = Path("alembic/env.py")

s = p.read_text()

old = "import src.models.saas_core\n"

new = "import src.models.saas_core\nimport src.feedback.models\n"

if old in s:
    s = s.replace(old,new,1)
    p.write_text(s)
    print("✅ feedback model added to alembic loader")
else:
    print("❌ saas_core import not found")
