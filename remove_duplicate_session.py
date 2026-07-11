from pathlib import Path
import re

file = Path("src/auth/router.py")
text = file.read_text()

pattern = re.compile(
    r'(create_login_session\([\s\S]*?\)\n\s*)(create_login_session\([\s\S]*?\)\n)',
    re.MULTILINE
)

text, count = pattern.subn(r'\1', text, count=1)

file.write_text(text)

print(f"REMOVED {count} DUPLICATE SESSION CALL")
