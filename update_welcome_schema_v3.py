from pathlib import Path

p = Path("src/domains/welcome/schemas.py")

s = p.read_text()

s = s.replace(
"""    banner_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None""",
"""    banner_active: bool = True

    logo_url: Optional[str] = None
    hero_image_url: Optional[str] = None
    theme_color: Optional[str] = "#2563eb"

    seo_title: Optional[str] = None
    seo_description: Optional[str] = None

    sections_json: Optional[list] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None"""
)


s = s.replace(
"""    banner_active: bool = True""",
"""    banner_active: bool = True

    logo_url: str = ""
    hero_image_url: str = ""
    theme_color: str = "#2563eb"

    seo_title: str = ""
    seo_description: str = ""

    sections_json: list = []"""
)


p.write_text(s)

print("WELCOME CMS V3 SCHEMA UPDATED")
