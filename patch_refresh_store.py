from pathlib import Path

file = Path("src/auth/router.py")
text = file.read_text()

old = '''    token_claims = {"user_id": user.id, "tenant_id": user.tenant_id, "role": user.role}
    return {'''

new = '''    token_claims = {"user_id": user.id, "tenant_id": user.tenant_id, "role": user.role}

    access_token = create_access_token(token_claims)
    refresh_token = create_refresh_token(token_claims)

    create_refresh_session(
        db=db,
        user=user,
        refresh_token=refresh_token,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,'''

text = text.replace(old, new, 1)

file.write_text(text)
print("REFRESH STORAGE PATCHED")
