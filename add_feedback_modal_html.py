from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

marker = """
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
"""

html = '''

<!-- FEEDBACK MODAL START -->

<div class="feedback-modal" id="feedbackModal">


<div class="feedback-modal-card">


<h3 id="feedbackTitle">
Feedback
</h3>


<input 
class="feedback-input"
id="feedbackSubject"
placeholder="Subject">


<textarea
class="feedback-input"
id="feedbackMessage"
rows="5"
placeholder="Write your feedback..."></textarea>


<button class="feedback-submit">
Send Feedback
</button>


<div class="feedback-close">
Close
</div>


</div>


</div>


<!-- FEEDBACK MODAL END -->

'''

if "FEEDBACK MODAL START" in s:
    print("⚠️ already exists")
elif marker in s:
    s=s.replace(marker, html+marker,1)
    p.write_text(s)
    print("✅ Feedback modal HTML added")
else:
    print("❌ marker not found")
