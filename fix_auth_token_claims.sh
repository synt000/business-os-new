python - <<'PY'
from pathlib import Path

p = Path("src/auth/router.py")

text = p.read_text()

old = '''    if tenant and tenant.trial_expired:
        raise HTTPException(status_code=402, detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED")

        token_claims = {"user_id": user.id, "tenant_id": user.tenant_id, "role": user.role}
'''

new = '''    if tenant and tenant.trial_expired:
        raise HTTPException(
            status_code=402,
            detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED"
        )

    token_claims = {
        "user_id": user.id,
        "tenant_id": user.tenant_id,
        "role": user.role
    }
'''

if old not in text:
    print("TARGET BLOCK NOT FOUND")
else:
    text = text.replace(old,new)
    p.write_text(text)
    print("FIXED token_claims indentation")
PY
