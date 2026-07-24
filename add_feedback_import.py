from pathlib import Path

p = Path("src/main.py")

s = p.read_text()

old = '''from src.domains.payment_gateway.router import router as payment_gateway_router
'''

new = '''from src.domains.payment_gateway.router import router as payment_gateway_router

from src.feedback.router import router as feedback_router
'''

if old in s:
    s = s.replace(old,new,1)
    p.write_text(s)
    print("✅ feedback router import added")
else:
    print("❌ import location not found")
