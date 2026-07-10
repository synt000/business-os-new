from pathlib import Path

p = Path("src/templates/login.html")
text = p.read_text()

insert = """
<script>
document.getElementById("loginForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    await login(email,password);
});
</script>
"""

if 'loginForm").addEventListener("submit"' not in text:
    text += insert
    p.write_text(text)
    print("LOGIN SUBMIT PATCHED")
else:
    print("ALREADY PATCHED")
