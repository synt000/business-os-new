from pathlib import Path

p = Path("src/product/router.py")
s = p.read_text()

start = s.find("    if invoice:\n        invoice.status = \"PAID\"")

if start == -1:
    print("PAYMENT SYNC LEFTOVER NOT FOUND")
    raise SystemExit

# Find next logical boundary
end = s.find("\n\n", start)

if end == -1:
    end = len(s)

s = s[:start] + s[end:]

p.write_text(s)

print("REMOVED PAYMENT SYNC LEFTOVER")
