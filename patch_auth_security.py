from pathlib import Path

file = Path("src/auth/router.py")

text = file.read_text()


imports = """
from src.security.login_guard import (
    check_account_locked,
    register_failed_login,
    register_success_login
)

from src.security.event_logger import log_security_event
"""


if "from src.security.login_guard import" not in text:
    text = text.replace(
        "from src.models.subscription import Subscription, SubscriptionPlan",
        "from src.models.subscription import Subscription, SubscriptionPlan\n" + imports
    )


file.write_text(text)

print("AUTH SECURITY IMPORT PATCHED")
