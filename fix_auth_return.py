from pathlib import Path

p = Path("src/auth/router.py")
text = p.read_text()

old = '''
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token": create_access_token(token_claims),
        "refresh_token": create_refresh_token(token_claims),
        "workspace_id": user.tenant_id,
        "role_profile": user.role
    }
'''

new = '''
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "workspace_id": user.tenant_id,
        "role_profile": user.role
    }
'''

if old in text:
    text = text.replace(old, new)
    p.write_text(text)
    print("AUTH LOGIN FIXED")
else:
    print("RETURN BLOCK NOT FOUND")
