from pathlib import Path

p = Path("src/main.py")
text = p.read_text(encoding="utf-8")

marker = "# DYNAMIC COMPATIBILITY INJECTOR FOR CORE ANALYTICS INTEGRATION"

patch = '''
# =====================================================
# FORCE EXPAND _IncludedRouter (FastAPI 0.118+/Py3.14)
# =====================================================
from fastapi.routing import _IncludedRouter

def _force_expand_routes(application):
    changed = True
    while changed:
        changed = False
        expanded = []

        for route in application.router.routes:
            if isinstance(route, _IncludedRouter):
                router = route.original_router
                ctx = route.include_context
                prefix = ctx.prefix or ""

                for child in router.routes:
                    if hasattr(child, "path"):
                        child.path = prefix + child.path
                    expanded.append(child)

                changed = True
            else:
                expanded.append(route)

        application.router.routes = expanded

_force_expand_routes(app)
print("✅ IncludedRouter auto-expanded at startup")
'''

if patch not in text:
    if marker in text:
        text = text.replace(marker, patch + "\n\n" + marker)
    else:
        text += "\n\n" + patch

p.write_text(text, encoding="utf-8")
print("✅ Startup route expansion injected.")
