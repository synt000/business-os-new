const API="/api/v4";

async function loadDashboard(){

    const token = localStorage.getItem("access_token");

    if(!token){
        location="/login";
        return;
    }

    const r = await fetch(API + "/dashboard/summary", {
        headers:{
            "Authorization":"Bearer " + token
        }
    });

    if(!r.ok){
        console.log(await r.text());
        return;
    }

    const d = await r.json();

    console.log("DASHBOARD DATA", d);

    const cards = document.querySelectorAll(".text-xl.font-bold.text-white");

    if(cards.length >= 4){
        cards[0].innerText = d.products ?? 0;
        cards[1].innerText = d.orders ?? 0;
        cards[2].innerText = d.customers ?? 0;
        cards[3].innerText = d.suppliers ?? 0;
    }
}

async function login(email, password){

    try{

        const r = await fetch(API + "/auth/login", {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                email:email,
                password:password
            })
        });

        const d = await r.json();

        if(!r.ok){
            alert(d.detail || "Login Failed");
            return;
        }

        localStorage.setItem("access_token", d.access_token);
        localStorage.setItem("tenant_id", d.workspace_id);
        localStorage.setItem("role_profile", d.role_profile);

        location="/dashboard";

    }catch(err){
        alert(err);
        console.error(err);
    }
}

function logout(){
    localStorage.clear();
    location="/login";
}

if(window.location.pathname === "/dashboard"){
    loadDashboard();
}

if(window.location.pathname === "/login"){

    const btn = document.getElementById("loginBtn");

    if(btn){
        btn.onclick = function(){
            login(
                document.getElementById("email").value,
                document.getElementById("password").value
            );
        };
    }
}
