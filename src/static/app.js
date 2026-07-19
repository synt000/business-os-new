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
        "role_profile",
        data.role_profile || "USER"
    );


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


// =====================================
// GLOBAL API FETCH WITH JWT
// =====================================

async function apiFetch(url, options={}){

    let token = localStorage.getItem(
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
        url,
        options
    );


    // Access token expired
    if(res.status === 401){

        let refresh =
            localStorage.getItem(
                "refresh_token"
            );


        if(!refresh){
            localStorage.clear();
            window.location.href="/login";
            return res;
        }


        let r = await fetch(
            "/api/v4/auth/refresh",
            {
                method:"POST",
                headers:{
                    "Content-Type":
                    "application/json"
                },
                body:JSON.stringify({
                    refresh_token: refresh
                })
            }
        );


        if(r.ok){

            let data =
                await r.json();


            saveTokens(data);


            options.headers.Authorization =
                "Bearer " +
                data.access_token;


            return await fetch(
                url,
                options
            );

        }else{

            localStorage.clear();
            window.location.href="/login";

        }

    }


    return res;
}

