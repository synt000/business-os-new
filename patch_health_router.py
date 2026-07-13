from pathlib import Path

p = Path("src/domains/dashboard/router.py")

s = p.read_text()

s = s.replace(
"get_ceo_dashboard_summary",
"get_ceo_dashboard_summary,\n    get_business_health_score"
)

old = '''return {
        "status": "SUCCESS",
        "health_score": 100,
        "level": "EXCELLENT"
    }'''

new = '''return {
        "status": "SUCCESS",
        "health": get_business_health_score(
            db,
            current_user.tenant_id
        )
    }'''

s = s.replace(old,new)

s = s.replace(
"current_user: User = Depends(get_current_user)                          ):",
"current_user: User = Depends(get_current_user),\n        db: Session = Depends(get_db)\n                          ):"
)

p.write_text(s)
print("health router patched")
