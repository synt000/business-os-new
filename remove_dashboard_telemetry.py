from pathlib import Path

p = Path("src/main.py")
text = p.read_text()

start = text.find(
    "# DYNAMIC COMPATIBILITY INJECTOR FOR CORE ANALYTICS INTEGRATION"
)

end = text.find(
    '@app.get("/api/v4/docs", include_in_schema=False)'
)

if start != -1 and end != -1:
    backup = Path(
        "src/main.py.before_remove_dashboard_telemetry"
    )

    backup.write_text(text)

    text = text[:start] + text[end:]

    p.write_text(text)

    print("REMOVED")
    print("BACKUP:", backup)

else:
    print("MARKER NOT FOUND")
    print("start:", start)
    print("end:", end)
