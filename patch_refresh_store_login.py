from pathlib import Path

file = Path("src/auth/router.py")
text = file.read_text()

first = text.find("create_refresh_session(")
second = text.find("token_claims =", first + 1)

if second != -1:
    end = text.find("return {", second)

    block = '''    token_claims = {"user_id": user.id, "tenant_id": user.tenant_id, "role": user.role}

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

    text = text[:second] + block + text[end + len("return {"):]

file.write_text(text)
print("LOGIN REFRESH STORAGE PATCHED")
