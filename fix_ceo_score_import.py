from pathlib import Path

p = Path("src/domains/ai_insight/router.py")

text = p.read_text(encoding="utf-8")

text = text.replace(
"""
from src.domains.ai_insight.recommendation import (
    generate_ai_recommendations,
    generate_ceo_score
)
""",
"""
from src.domains.ai_insight.recommendation import (
    generate_ai_recommendations
)

from src.domains.ai_insight.service import (
    generate_ceo_score
)
"""
)

p.write_text(text, encoding="utf-8")

print("✅ Fixed CEO Score import")
