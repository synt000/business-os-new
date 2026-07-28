from pathlib import Path

p = Path("src/domains/welcome/models.py")

s = p.read_text()

old = """    banner_active = Column(
        Boolean,
        default=True
    )
"""

new = """    banner_active = Column(
        Boolean,
        default=True
    )

    logo_url = Column(
        Text,
        nullable=True
    )

    hero_image_url = Column(
        Text,
        nullable=True
    )

    theme_color = Column(
        String,
        default="#2563eb"
    )

    seo_title = Column(
        Text,
        nullable=True
    )

    seo_description = Column(
        Text,
        nullable=True
    )

    sections_json = Column(
        Text,
        nullable=True
    )
"""

if old in s:
    s = s.replace(old,new)
    p.write_text(s)
    print("WELCOME CMS V3 MODEL UPDATED")
else:
    print("TARGET BLOCK NOT FOUND")
