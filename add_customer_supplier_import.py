from pathlib import Path

p = Path("src/telegram_bot/callbacks/registry.py")
s = p.read_text()

add = """
from .customer_actions import (
    customer_list_callback,
    customer_add_callback,
    customer_analysis_callback
)

from .supplier_actions import (
    supplier_list_callback,
    supplier_add_callback,
    supplier_analysis_callback
)
"""

if "from .customer_actions import" not in s:
    s = s.replace(
        "from .users_center import users_list_callback, rbac_roles_callback, permissions_callback",
        "from .users_center import users_list_callback, rbac_roles_callback, permissions_callback\n" + add
    )

p.write_text(s)
