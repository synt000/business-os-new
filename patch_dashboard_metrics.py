from pathlib import Path

p=Path("src/static/app.js")
t=p.read_text()

start=t.find("async function loadDashboard(){")
end=t.find("}\n\nasync function login", start)

new="""async function loadDashboard(){

    const token = localStorage.getItem("access_token");

    const r = await fetch(API + "/dashboard/summary", {
        headers:{
            "Authorization":"Bearer " + token
        }
    });

    const d = await r.json();

    console.log("DASHBOARD DATA", d);

    const cards = document.querySelectorAll(".text-xl.font-bold.text-white");

    if(cards.length >= 3){

        cards[0].innerText = "$" + d.total_revenue_usd;
        cards[1].innerText = d.active_tenants;
        cards[2].innerText = d.operational_nodes_health;

    }

}
"""

if start != -1 and end != -1:
    t=t[:start]+new+t[end+2:]
    p.write_text(t)
    print("dashboard binding patched")
else:
    print("target not found")
