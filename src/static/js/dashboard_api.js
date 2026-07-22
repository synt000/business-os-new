console.log("DASHBOARD_API_LOADED");
async function loadDashboardWidgets(){

try{

const token =
localStorage.getItem("access_token");


const res = await fetch(
"/api/v4/dashboard/widgets",
{
headers:{
"Authorization":"Bearer "+token
}
});


const data = await res.json();

console.log(
"DASHBOARD WIDGET DATA",
data
);


const today = data.today || {};


if(document.getElementById("today-orders")){
document.getElementById("today-orders").innerText =
today.today_orders || 0;
}


if(document.getElementById("today-revenue")){
document.getElementById("today-revenue").innerText =
(today.today_revenue || 0).toLocaleString()+" MMK";
}


if(document.getElementById("new-customers")){
document.getElementById("new-customers").innerText =
today.new_customers || 0;
}


if(document.getElementById("low-stock")){
document.getElementById("low-stock").innerText =
today.low_stock || 0;
}


if(document.getElementById("social-leads")){
document.getElementById("social-leads").innerText =
today.social_leads || 0;
}


if(document.getElementById("notifications")){
document.getElementById("notifications").innerText =
today.notifications || 0;
}


}

catch(e){

console.error(
"DASHBOARD WIDGET ERROR",
e
);

}

}


document.addEventListener(
"DOMContentLoaded",
loadDashboardWidgets
);


// PREMIUM DASHBOARD METRICS
const widgets = data.widgets || {};

const revenueValue =
    today.today_revenue ||
    (widgets.sales && widgets.sales.today_revenue) ||
    0;

const ordersValue =
    today.today_orders ||
    (widgets.sales && widgets.sales.today_orders) ||
    0;

const customerValue =
    today.new_customers ||
    (widgets.customer && widgets.customer.total_customers) ||
    0;

const productValue =
    (widgets.inventory && widgets.inventory.total_products) ||
    0;


if(document.getElementById("revenue")){
    document.getElementById("revenue").innerText =
    Number(revenueValue).toLocaleString()+" MMK";
}

if(document.getElementById("orders")){
    document.getElementById("orders").innerText =
    ordersValue;
}

if(document.getElementById("customers")){
    document.getElementById("customers").innerText =
    customerValue;
}

if(document.getElementById("products")){
    document.getElementById("products").innerText =
    productValue;
}

