from pathlib import Path

p = Path("src/domains/welcome/schemas.py")

s = p.read_text()

s = s.replace(
"""    faq_content: Optional[str] = None
    live_banner: Optional[str] = None
    banner_active: bool = True""",
"""    faq_content: Optional[str] = None
    features_json: Optional[str] = None
    button_text: Optional[str] = None
    live_banner: Optional[str] = None
    banner_active: bool = True"""
)

s = s.replace(
"""    faq_content: str = ""
    live_banner: str = "Welcome to Business OS"
    banner_active: bool = True""",
"""    faq_content: str = ""
    features_json: str = "[]"
    button_text: str = "Continue"
    live_banner: str = "Welcome to Business OS"
    banner_active: bool = True"""
)

p.write_text(s)

print("WELCOME SCHEMA V2 UPDATED")
