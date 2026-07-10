const API="/api/v4";

async function loadDashboard(){

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

async function login(email, password){
    alert("login() called");

    try{
        const r = await fetch(API + "/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        alert("HTTP Status: " + r.status);

        const d = await r.json();

        alert(JSON.stringify(d));
        if(r.ok){

            localStorage.setItem(
                "access_token",
                d.access_token
            );

            if(d.workspace_id){
                localStorage.setItem(
                    "tenant_id",
                    d.workspace_id
                );
            }

            if(d.role_profile){
                localStorage.setItem(
                    "role_profile",
                    d.role_profile
                );
            }

            location="/dashboard";

        }

    }catch(err){

        alert("FETCH ERROR: " + err);
        console.error(err);

    }
}


function logout(){

    localStorage.clear();
    location="/login";

}




window.onload = function(){
    alert('PATH: ' + window.location.pathname);

    if(window.location.pathname === "/dashboard"){

        loadDashboard();

    }


    if(window.location.pathname === "/login"){

        const btn = document.getElementById("loginBtn");

        if(btn){

            btn.onclick = async function(){

                await login(
                    document.getElementById("email").value,
                    document.getElementById("password").value
                );

            };

        }

    }

};
