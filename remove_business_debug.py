from pathlib import Path

p = Path("src/dashboard/router.py")

s = p.read_text()

old = """
    for b in businesses:
        print(
            "NAME:",
            b.business_name,
            "TYPE:",
            b.business_type_code
        )

    print(
        "SELECTED:",
        business.business_name if business else None,
        business.business_type_code if business else None
    )
"""

s = s.replace(old, "")

p.write_text(s)

print("BUSINESS DEBUG REMOVED")
