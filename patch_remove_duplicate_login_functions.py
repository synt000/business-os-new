from pathlib import Path
import re

file = Path("src/auth/router.py")

text = file.read_text()

patterns = [
    r"def check_login_security\(user\):.*?db\.commit\(\)\n",
    r"def register_failed_login\(user,\s*db\):.*?db\.commit\(\)\n",
    r"def register_success_login\(user,\s*db\):.*?db\.commit\(\)\n",
]

for pattern in patterns:
    text = re.sub(pattern, "", text, flags=re.S)

file.write_text(text)

print("DUPLICATE LOGIN FUNCTIONS REMOVED")
