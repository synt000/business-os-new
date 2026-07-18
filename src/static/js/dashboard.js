async function loadCEOStats(){

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


try{

const res = await fetch(
"/ceo-summary",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


const data = await res.json();


console.log(
"CEO DASHBOARD",
data
);


if(data.status==="SUCCESS"){

const d=data.dashboard;


if(document.getElementById("revenue")){
document.getElementById("revenue").innerText =
Number(d.today_revenue).toLocaleString()+" MMK";
}


if(document.getElementById("orders")){
document.getElementById("orders").innerText =
d.today_orders;
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


}catch(e){

console.error(
"CEO DASHBOARD ERROR",
e
);

}


}


document.addEventListener(
"DOMContentLoaded",
loadCEOStats
);
