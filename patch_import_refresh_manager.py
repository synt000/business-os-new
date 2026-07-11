from pathlib import Path

file = Path("src/auth/router.py")
text = file.read_text()

import_line = "from src.security.refresh_manager import create_refresh_session\n"

if import_line not in text:
    text = text.replace(
        "from src.security.session_manager import create_login_session\n",
        "from src.security.session_manager import create_login_session\n"
        + import_line
    )

file.write_text(text)
print("REFRESH MANAGER IMPORT ADDED")
