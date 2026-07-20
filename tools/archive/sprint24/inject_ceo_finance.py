from pathlib import Path

p = Path("src/domains/dashboard/router.py")

text = p.read_text()

old = '''    return {
        "status": "SUCCESS",
        "dashboard": get_ceo_dashboard_summary(
            db,
            current_user.tenant_id
        )
    }'''

new = '''    return {
        "status": "SUCCESS",
        "dashboard": get_ceo_dashboard_summary(
            db,
            current_user.tenant_id
        ),
        "finance": get_finance_insight(
            db,
            current_user.tenant_id
        )
    }'''

if old not in text:
    print("❌ target not found")
else:
    text = text.replace(old,new)
    p.write_text(text)
    print("✅ CEO finance injected")
