from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

marker = '''<!-- RECENT ACTIVITY START -->'''

html = '''
<!-- FEEDBACK CENTER START -->

<section class="feedback-section">

<div class="section-header">

<h2 class="section-title">
💬 Feedback Center
</h2>

</div>


<div class="feedback-card">

<div class="feedback-grid">


<div class="feedback-btn">

<div class="feedback-icon">
🐞
</div>

<div class="feedback-text">
Report Bug
</div>

</div>



<div class="feedback-btn">

<div class="feedback-icon">
💡
</div>

<div class="feedback-text">
Suggest Feature
</div>

</div>



<div class="feedback-btn">

<div class="feedback-icon">
⭐
</div>

<div class="feedback-text">
Rate Experience
</div>

</div>


</div>

</div>

</section>


<!-- FEEDBACK CENTER END -->


'''

if "FEEDBACK CENTER START" in s:
    print("⚠️ already exists")
elif marker in s:
    s=s.replace(marker, html + marker, 1)
    p.write_text(s)
    print("✅ Feedback Center HTML added")
else:
    print("❌ marker not found")
