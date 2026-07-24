from pathlib import Path

p=Path("src/templates/dashboard.html")

s=p.read_text()

old='<script src="/static/js/dashboard_api.js?v=7.3"></script>'

new='''<script src="/static/js/feedback.js"></script>

<script src="/static/js/dashboard_api.js?v=7.3"></script>'''

if "feedback.js" not in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ feedback.js included")
else:
    print("⚠️ already included")
