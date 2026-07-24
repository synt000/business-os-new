from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

s=s.replace(
'<div class="feedback-btn">\n\n<div class="feedback-icon">\n🐞',
'<div class="feedback-btn" id="reportBugBtn">\n\n<div class="feedback-icon">\n🐞',
1
)

s=s.replace(
'<div class="feedback-btn">\n\n<div class="feedback-icon">\n💡',
'<div class="feedback-btn" id="featureBtn">\n\n<div class="feedback-icon">\n💡',
1
)

s=s.replace(
'<div class="feedback-btn">\n\n<div class="feedback-icon">\n⭐',
'<div class="feedback-btn" id="rateBtn">\n\n<div class="feedback-icon">\n⭐',
1
)

p.write_text(s)

print("✅ Feedback button IDs added")
