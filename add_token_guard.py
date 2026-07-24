from pathlib import Path

p = Path("src/static/js/dashboard_api.js")

s = p.read_text()

old = '''if(!res.ok){

    console.error(
        "Dashboard API failed:",
        res.status
    );

    const errorBox = document.getElementById(
        "dashboard-error"
    );

    if(errorBox){

        errorBox.style.display = "block";

        errorBox.innerText =
        "⚠️ Dashboard temporarily unavailable. Please try again.";

    }

    return;
}'''

new = '''if(!res.ok){

    console.error(
        "Dashboard API failed:",
        res.status
    );


    if(res.status === 401){

        localStorage.removeItem("access_token");
        localStorage.removeItem("tenant_id");


        alert(
            "🔐 Session expired. Please login again."
        );


        window.location.href = "/login";

        return;

    }


    const errorBox = document.getElementById(
        "dashboard-error"
    );

    if(errorBox){

        errorBox.style.display = "block";

        errorBox.innerText =
        "⚠️ Dashboard temporarily unavailable. Please try again.";

    }

    return;
}'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ Token expiry guard added")
else:
    print("❌ block not found")
