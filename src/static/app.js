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


    location="/dashboard";

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
