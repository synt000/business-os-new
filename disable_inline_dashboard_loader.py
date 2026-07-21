from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text()

old = '''document.addEventListener(
"DOMContentLoaded",
()=>{

    if(typeof apiFetch === "function"){

        setTimeout(()=>{

            loadOwnerDashboard();
            loadFinanceInsight();
            loadDashboardWidgets();

        },1000);


        setInterval(
            loadOwnerDashboard,
            30000
        );


        setInterval(
            loadFinanceInsight,
            30000
        );

    }

});'''

new = '''/*
document.addEventListener(
"DOMContentLoaded",
()=>{

    if(typeof apiFetch === "function"){

        setTimeout(()=>{

            loadOwnerDashboard();
            loadFinanceInsight();
            loadDashboardWidgets();

        },1000);


        setInterval(
            loadOwnerDashboard,
            30000
        );


        setInterval(
            loadFinanceInsight,
            30000
        );

    }

});
*/'''

if old not in text:
    raise SystemExit("TARGET BLOCK NOT FOUND")

text = text.replace(old,new)

p.write_text(text)

print("DONE")
