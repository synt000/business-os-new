from pathlib import Path

p = Path("src/domains/purchase/router.py")
s = p.read_text()

start = s.index("    for item in items:")
end = s.index("    db.commit()", start)

replacement = """    # STOCK RECEIVE moved to /receive endpoint
    # approve only changes status

"""

s = s[:start] + replacement + s[end:]

p.write_text(s)

print("FIXED")
