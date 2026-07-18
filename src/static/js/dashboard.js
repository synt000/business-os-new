async function loadDashboardSummary(){

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const res = await fetch(
            "/api/v4/dashboard/summary",
            {
                headers:{
                    "Authorization":"Bearer "+token
                }
            }
        );


        const data = await res.json();

        console.log(
            "DASHBOARD SUMMARY",
            data
        );


        if(data.revenue !== undefined){

            const revenue =
            document.getElementById("revenue");

            if(revenue){
                revenue.innerText =
                data.revenue.toLocaleString()
                +" MMK";
            }
        }


        const orders =
        document.getElementById("orders");

        if(orders){
            orders.innerText =
            data.orders;
        }


        const inventory =
        document.getElementById("inventory");

        if(inventory){
            inventory.innerText =
            data.products;
        }


    }
    catch(e){

        console.error(
            "Dashboard API Error",
            e
        );

    }

}


loadDashboardSummary();
