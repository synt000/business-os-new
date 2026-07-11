from pathlib import Path

p = Path("src/auth/router.py")
s = p.read_text()

s = s.replace(
'''    if tenant and tenant.trial_expired:
        raise HTTPException(status_code=402, detail="WORKSPACE_LOCKED: FREE_TRIAL_EXPIRED")

        token_claims = {"user_id": user.id, "tenant_id": user.tenant_id, "role": user.role}
''',
'''    if tenant and tenant.trial_expired:
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
)

p.write_text(s)

print("DONE")
