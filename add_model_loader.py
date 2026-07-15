from pathlib import Path

p = Path("src/main.py")
text = p.read_text()

marker = "from src.core.config import settings"

insert = """# ==========================================
# SQLAlchemy Model Registry Preload
# ==========================================
import src.models
import src.domains.product.models
import src.domains.category.models
"""

if "SQLAlchemy Model Registry Preload" not in text:
    text = text.replace(marker, insert + "\n" + marker)
    p.write_text(text)
    print("Model Loader Added ✅")
else:
    print("Already Added ✅")
