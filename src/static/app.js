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
