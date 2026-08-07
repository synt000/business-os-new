from pathlib import Path

p = Path("src/product/router.py")

s = p.read_text()

start = s.find('        db.add(AuditLog(\n            tenant_id=current_user.tenant_id,\n            action="UPDATE",\n            table_name="invoices"')

if start == -1:
    print("ORPHAN BLOCK NOT FOUND")
    raise SystemExit

end_marker = '        ))'

end = s.find(end_marker, start)

if end == -1:
    print("END MARKER NOT FOUND")
    raise SystemExit

end += len(end_marker)

s = s[:start] + s[end:]

p.write_text(s)

print("REMOVED ORPHAN INVOICE AUDIT BLOCK")
