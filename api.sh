#!/data/data/com.termux/files/usr/bin/bash

TOKEN=$(python - <<'PY'
import json
print(json.load(open(".auth.json"))["access_token"])
PY
)

curl "$1" \
-H "Authorization: Bearer $TOKEN"
