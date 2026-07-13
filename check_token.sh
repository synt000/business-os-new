echo "===== ACCESS TOKEN ====="
python - <<'PY'
import json
from pathlib import Path

try:
    print("token.json:")
    print(json.loads(Path("token.json").read_text()).get("access_token","NOT FOUND"))
except Exception as e:
    print("token.json not found")

print("\nlocalStorage is browser-side only.")
PY
