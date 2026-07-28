from pathlib import Path

p = Path("src/domains/welcome/models.py")

s = p.read_text()

s = s.replace(
"""    faq_content = Column(
        Text,
        nullable=True
    )

    live_banner = Column(
        Text,
        nullable=True
    )""",
"""    faq_content = Column(
        Text,
        nullable=True
    )

    features_json = Column(
        Text,
        nullable=True
    )

    button_text = Column(
        String,
        nullable=True,
        default="Continue"
    )

    live_banner = Column(
        Text,
        nullable=True
    )"""
)

p.write_text(s)

print("WELCOME MODEL V2 UPDATED")
