from pathlib import Path

file = Path("src/auth/router.py")
text = file.read_text()

# -------------------------------------------------
# Import Request
# -------------------------------------------------
if "Request," not in text:
    text = text.replace(
        "from fastapi import APIRouter, Depends, HTTPException, status",
        "from fastapi import APIRouter, Depends, HTTPException, status, Request"
    )

# -------------------------------------------------
# Import Session Manager
# -------------------------------------------------
if "create_login_session" not in text:
    text = text.replace(
        "from src.security.event_logger import log_security_event",
        "from src.security.event_logger import log_security_event\nfrom src.security.session_manager import create_login_session"
    )

# -------------------------------------------------
# OAuth2 Login
# -------------------------------------------------
text = text.replace(
    "db: Session = Depends(get_db)",
    "request: Request,\n    db: Session = Depends(get_db)",
    1
)

text = text.replace(
    "register_success_login(db, user)",
    """register_success_login(db, user)

    create_login_session(
        db=db,
        user=user,
        ip_address=request.client.host if request.client else "UNKNOWN",
        user_agent=request.headers.get("user-agent","UNKNOWN"),
        device_name=request.headers.get("user-agent","UNKNOWN"),
    )""",
    1
)

# -------------------------------------------------
# JSON Login
# -------------------------------------------------
marker = "payload: JSONLoginInboundPayload,"
idx = text.find(marker)

if idx != -1:
    idx2 = text.find("db: Session = Depends(get_db)", idx)
    if idx2 != -1:
        text = (
            text[:idx2]
            + "request: Request,\n    "
            + text[idx2:]
        )

text = text.replace(
    "register_success_login(db, user)",
    """register_success_login(db, user)

    create_login_session(
        db=db,
        user=user,
        ip_address=request.client.host if request.client else "UNKNOWN",
        user_agent=request.headers.get("user-agent","UNKNOWN"),
        device_name=request.headers.get("user-agent","UNKNOWN"),
    )""",
    1
)

file.write_text(text)

print("AUTH ROUTER SESSION PATCHED")
