from pathlib import Path

file = Path("src/auth/refresh_router.py")
text = file.read_text()

text = text.replace(
    "decode_token,",
    "verify_refresh_token,"
)

text = text.replace(
    "claims = decode_token(payload.refresh_token)",
    "claims = verify_refresh_token(payload.refresh_token)"
)

file.write_text(text)
print("REFRESH VERIFY PATCHED")
