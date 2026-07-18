async function loadDashboardSummary(){

try{

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


const res = await fetch(
"/ceo-summary",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


const data = await res.json();


console.log("CEO DASHBOARD",data);


if(data.dashboard){


const d=data.dashboard;


if(document.getElementById("revenue")){
document.getElementById("revenue").innerText =
Number(d.today_revenue).toLocaleString()+" MMK";
}


if(document.getElementById("orders")){
document.getElementById("orders").innerText =
d.today_orders+" Orders";
}


if(document.getElementById("customers")){
document.getElementById("customers").innerText =
d.total_customers;
}


if(document.getElementById("products")){
document.getElementById("products").innerText =
d.total_products;
}


}


}
catch(e){

console.error(
"DASHBOARD API ERROR",
e
);

}

}


document.addEventListener(
"DOMContentLoaded",
loadDashboardSummary
);
