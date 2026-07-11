from pathlib import Path

p = Path("src/models/saas_core.py")

text = p.read_text()

if "from src.domains.inventory import models as inventory_models" not in text:
    text = text.replace(
        "from src.core.database import Base",
        "from src.core.database import Base\nfrom src.domains.inventory import models as inventory_models"
    )

p.write_text(text)

print("DONE")
