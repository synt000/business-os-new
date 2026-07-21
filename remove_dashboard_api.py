from pathlib import Path
import re

p = Path("src/dashboard/router.py")
text = p.read_text()

backup = Path("src/dashboard/router.py.before_dashboard_api_cleanup")
backup.write_text(text)

patterns = [
    r'@router\.get\("/api/v4/dashboard/today-stats"\).*?(?=\n@router|\Z)',
    r'@router\.get\("/api/v4/dashboard/widgets"\).*?(?=\n@router|\Z)',
    r'@router\.get\("/api/v4/dashboard/revenue-chart"\).*?(?=\n@router|\Z)',
]

for pat in patterns:
    text = re.sub(pat, "", text, flags=re.S)

p.write_text(text)

print("✅ Dashboard duplicate APIs removed")
print("✅ Backup:", backup)
