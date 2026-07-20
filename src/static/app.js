const API="/api/v4";


async function loadDashboard(){

    const token =
    localStorage.getItem("access_token");


    if(!token){
        location="/login";
        return;
    }


    const res = await fetch(
        API + "/dashboard/summary",
        {
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    if(!res.ok){

        console.log(
            await res.text()
        );

        return;
    }


    const data =
    await res.json();


    console.log(
        "Dashboard:",
        data
    );


    const products =
    document.getElementById("products");

    const orders =
    document.getElementById("orders");

    const customers =
    document.getElementById("customers");

    const suppliers =
    document.getElementById("suppliers");


    if(products)
        products.innerText =
        data.products ?? 0;


    if(orders)
        orders.innerText =
        data.orders ?? 0;


    if(customers)
        customers.innerText =
        data.customers ?? 0;


    if(suppliers)
        suppliers.innerText =
        data.suppliers ?? 0;

}




async function login(
    email,
    password
){

    const res =
    await fetch(
        API + "/auth/login",
        {
            method:"POST",
            headers:{
                "Content-Type":
                "application/json"
            },
            body:JSON.stringify(
                {
                    email,
                    password
                }
            )
        }
    );


    const data =
    await res.json();


    if(!res.ok){

        alert(
            data.detail ||
            "Login Failed"
        );

        return;
    }


    localStorage.setItem(
        "access_token",
        data.access_token
    );

    localStorage.setItem(
        "refresh_token",
        data.refresh_token
    );

    localStorage.setItem(
        "workspace_id",
        data.workspace_id || ""
    );
    localStorage.setItem(
        "role_profile",
        data.role_profile || "USER"
    );

    saveAuth({
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        workspace_id: data.workspace_id || "",
        role_profile: data.role_profile || "USER"
    });


    let role = data.role_profile;


    if(!role && data.access_token){

        try{

            const payload =
            JSON.parse(
                atob(
                    data.access_token.split(".")[1]
                )
            );

            role = payload.role;

        }catch(e){

            console.log("JWT decode failed",e);

        }

    }


    localStorage.setItem(
        "role_profile",
        role || "USER"
    );


    if(role === "OWNER"){

        location="/owner";

    }
    else if(role === "ADMIN"){

        location="/admin";

    }
    else{

        location="/dashboard";

    }

}




function logout(){

    localStorage.clear();

    location="/login";

}



if(
window.location.pathname === "/dashboard"
){

    loadDashboard();

}


// =====================================
// JWT AUTO TOKEN HANDLER
// =====================================

function saveTokens(data){

    if(data.access_token){
        localStorage.setItem(
            "access_token",
            data.access_token
        );
    }

    if(data.refresh_token){
        localStorage.setItem(
            "refresh_token",
            data.refresh_token
        );
    }
}


// ===============================
// JWT AUTO REFRESH MANAGER
// ===============================

const AUTH_KEY = "business_os_auth";


function saveAuth(data) {
    localStorage.setItem(
        AUTH_KEY,
        JSON.stringify(data)
    );
}


function getAuth() {
    const data = localStorage.getItem(AUTH_KEY);
    return data ? JSON.parse(data) : null;
}


function clearAuth() {
    localStorage.removeItem(AUTH_KEY);
}


// Auto authenticated fetch
async function apiFetch(url, options = {}) {

    let auth = getAuth();

    // fallback for login flow
    if(!auth){
        auth = {
            access_token:
                localStorage.getItem("access_token"),
            refresh_token:
                localStorage.getItem("refresh_token")
        };
    }

    options.headers = {
        ...(options.headers || {}),
        "Authorization":
            auth?.access_token
            ? `Bearer ${auth.access_token}`
            : "",
        "Content-Type":
            "application/json"
    };


    let response = await fetch(url, options);


    // Token expired
    if (response.status === 401 && auth?.refresh_token) {

        const refreshResponse =
            await fetch(
                "/api/v4/auth/refresh?refresh_token="
                + encodeURIComponent(auth.refresh_token),
                {
                    method: "POST"
                }
            );


        if (refreshResponse.ok) {

            const refreshed =
                await refreshResponse.json();


            auth.access_token =
                refreshed.access_token;


            saveAuth(auth);


            options.headers.Authorization =
                `Bearer ${auth.access_token}`;


            response =
                await fetch(url, options);
        }

        else {
            clearAuth();
            window.location.href="/login";
        }
    }


    return response;
}


console.log(
    "✅ JWT Auto Refresh Manager Loaded"
);
