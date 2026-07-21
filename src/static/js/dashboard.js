
async function loadCEOStats(){

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");

    try{

        const res = await fetch(
            "/api/v4/dashboard/summary",
            {
                headers:{
                    "Authorization":"Bearer " + token
                }
            }
        );

        const data = await res.json();

        console.log(
            "BUSINESS DASHBOARD",
            data
        );

        if(data){

            const d = data.dashboard || data;


            const revenue =
                document.getElementById("revenue");

            const customers =
                document.getElementById("customers");

            const products =
                document.getElementById("products");

            const heroSales =
                document.getElementById("heroSales");

            const heroOrders =
                document.getElementById("heroOrders");


            if(revenue){
                revenue.innerText =
                    Number(d.revenue || 0)
                    .toLocaleString()+" MMK";
            }


            if(customers){
                customers.innerText =
                    d.customers || 0;
            }


            if(products){
                products.innerText =
                    d.products || 0;
            }


            if(heroSales){
                heroSales.innerText =
                    Number(d.revenue || 0)
                    .toLocaleString()+" MMK";
            }


            if(heroOrders){
                heroOrders.innerText =
                    d.orders || 0;
            }


            const todayOrders =
                document.getElementById("today-orders");

            const todayRevenue =
                document.getElementById("today-revenue");

            const newCustomers =
                document.getElementById("new-customers");

            const lowStock =
                document.getElementById("low-stock");

            const socialLeads =
                document.getElementById("social-leads");

            const notifications =
                document.getElementById("notifications");


            if(todayOrders){
                todayOrders.innerText =
                    d.today_orders || 0;
            }

            if(todayRevenue){
                todayRevenue.innerText =
                    Number(d.today_revenue || 0)
                    .toLocaleString();
            }

            if(newCustomers){
                newCustomers.innerText =
                    d.customers || 0;
            }

            if(lowStock){
                lowStock.innerText =
                    d.low_stock || 0;
            }

            if(socialLeads){
                socialLeads.innerText =
                    d.social_leads || 0;
            }

            if(notifications){
                notifications.innerText =
                    d.notifications || 0;
            }

        }


    }catch(e){

        console.error(
            "BUSINESS DASHBOARD ERROR",
            e
        );

    }

}

document.addEventListener(
    "DOMContentLoaded",
    loadCEOStats
);


async function loadAIProcurement(){

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


const box = document.getElementById("aiPurchaseList");

if(!box) return;


try{

const res = await fetch(
"/ai/purchases/pending",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


const data = await res.json();


if(
data.status==="SUCCESS" &&
data.items.length > 0
){

box.innerHTML = "";


data.items.forEach(po=>{


box.innerHTML += `

<div class="ai-po">

<div>
<b>${po.purchase_number}</b>
</div>

<div>
Amount:
${Number(po.amount).toLocaleString()} MMK
</div>

<div>
Status:
${po.status}
</div>


<button
class="ai-btn"
onclick="approveAIPO('${po.id}')">
✅ Approve
</button>


<button
class="ai-btn"
onclick="rejectAIPO('${po.id}')">
❌ Reject
</button>


</div>

`;


});


}else{


box.innerHTML =
"No Pending AI Purchase";


}


}catch(e){

console.error(
"AI PROCUREMENT ERROR",
e
);

box.innerHTML =
"AI Load Failed";

}


}



async function approveAIPO(id){

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


await fetch(
"/purchases/approve-ai-po/"+id,
{
method:"POST",
headers:{
"Authorization":"Bearer "+token
}
}
);


loadAIProcurement();

}



async function rejectAIPO(id){

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


await fetch(
"/ai/purchases/reject/"+id,
{
method:"POST",
headers:{
"Authorization":"Bearer "+token,
"Content-Type":"application/json"
},
body:JSON.stringify({
reason:"Rejected from Dashboard"
})
}
);


loadAIProcurement();

}



document.addEventListener(
"DOMContentLoaded",
loadAIProcurement
);

