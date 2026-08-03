const API="/api/v4";

async function login(email,password){
    const res = await fetch(
        API+"/auth/login",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                email,
                password
            })
        }
    );

    const data = await res.json();
    console.log("LOGIN RESPONSE:", data);

    if(data.access_token){
        localStorage.setItem(
            "access_token",
            data.access_token
        );

        if(data.workspace_id){
            localStorage.setItem(
                "tenant_id",
                data.workspace_id
            );
        }

        location="/dashboard";
    }
}


// ===============================
// Global Logout Handler
// ===============================
window.logout = function(){

    localStorage.removeItem("access_token");
    localStorage.removeItem("tenant_id");
    localStorage.removeItem("role_profile");

    window.location.href="/login";

};


document.addEventListener("DOMContentLoaded", function(){

    const btn = document.getElementById("logoutBtn");

    if(btn){
        btn.onclick = logout;
    }

});


// =====================================
// GLOBAL API FETCH WITH JWT
// =====================================

async function apiFetch(url, options={}){

    const token = localStorage.getItem(
        "access_token"
    );


    options.headers = {
        ...(options.headers || {}),
        "Authorization":
            "Bearer " + token,
        "Content-Type":
            "application/json"
    };


    let res = await fetch(
        "/api/v4" + url,
        options
    );


    if(res.status === 401){

        const refresh =
            localStorage.getItem(
                "refresh_token"
            );


        if(!refresh){

            localStorage.clear();

            window.location.href="/login";

            return res;

        }


        const refreshRes =
        await fetch(
            "/api/v4/auth/refresh",
            {
                method:"POST",
                headers:{
                    "Content-Type":
                    "application/json"
                },
                body:
                JSON.stringify({
                    refresh_token:
                    refresh
                })
            }
        );


        if(refreshRes.ok){

            const data =
            await refreshRes.json();


            if(data.access_token){

                localStorage.setItem(
                    "access_token",
                    data.access_token
                );


                return fetch(
                    "/api/v4"+url,
                    options
                );

            }

        }

    }


    return res;

}


async function loadWorkspaceMenu(){

    const token = localStorage.getItem("access_token");

    if(!token) return;

    const res = await fetch(
        "/api/workspace/menu",
        {
            headers:{
                "Authorization":"Bearer " + token
            }
        }
    );

    if(!res.ok) return;

    const data = await res.json();
    console.log("LOGIN RESPONSE:", data);

    const box=document.getElementById("dynamicMenu");

    if(!box) return;

    data.menu.forEach(item=>{

        const btn=document.createElement("button");

        btn.innerText=item.name;

        btn.onclick=function(){
            location.href=item.url;
        };

        box.appendChild(btn);

    });

}


document.addEventListener(
"DOMContentLoaded",
function(){
    loadWorkspaceMenu();
}
);

