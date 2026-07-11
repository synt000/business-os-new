from pathlib import Path
import re

file = Path("src/auth/router.py")
text = file.read_text()

text = re.sub(
    r"def register_success_login\(db,\s*user\):.*?db\.commit\(\)\n",
    "",
    text,
    flags=re.S,
)

file.write_text(text)

print("LAST DUPLICATE FUNCTION REMOVED")
