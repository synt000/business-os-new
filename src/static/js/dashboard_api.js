async function loadDashboardWidgets(){

try{

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


const res = await fetch(
"/api/v4/dashboard/widgets",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


const data = await res.json();

console.log("BUSINESS DASHBOARD",data);


const widgets = data.widgets || {};
const today = data.today || {};


if(document.getElementById("revenue")){
document.getElementById("revenue").innerText =
Number(
today.today_revenue || 0
).toLocaleString()+" MMK";
}


if(document.getElementById("orders")){
document.getElementById("orders").innerText =
(today.today_orders || 0)+" Orders";
}


if(document.getElementById("customers")){
document.getElementById("customers").innerText =
(today.new_customers || 0);
}


if(document.getElementById("products")){

let inventory =
widgets.inventory ||
widgets.low_stock ||
{};

document.getElementById("products").innerText =
inventory.total_products ||
inventory.count ||
0;

}


}
catch(e){

console.error(
"DASHBOARD WIDGET API ERROR",
e
);

}

}


document.addEventListener(
"DOMContentLoaded",
loadDashboardWidgets
);
