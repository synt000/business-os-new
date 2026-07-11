from pathlib import Path

p = Path("src/auth/router.py")
s = p.read_text()

start = s.index("    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()", s.index("async def authenticate_via_pure_json_payload"))

end = s.index("    access_token = create_access_token(token_claims)", start)

new_block = '''    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()

    if tenant and tenant.trial_expired:
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

s = s[:start] + new_block + s[end:]

p.write_text(s)

print("FORCE FIX DONE")
