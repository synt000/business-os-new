from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

text = text.replace(
    "loadRevenueExpense();",
    """
window.addEventListener(
"load",
function(){
loadRevenueExpense();
}
);
"""
)

p.write_text(text, encoding="utf-8")
print("✅ Revenue Chart delayed until page load")
