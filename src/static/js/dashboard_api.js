async function loadDashboardSummary(){

try{

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


const res = await fetch(
"/api/v4/dashboard/summary",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


const data = await res.json();

console.log("DASHBOARD SUMMARY",data);



if(data.revenue !== undefined){

document.getElementById("revenue").innerText =
Number(data.revenue).toLocaleString()+" MMK";

}


if(data.orders !== undefined){

document.getElementById("orders").innerText =
data.orders+" Processed";

}


if(data.products !== undefined){

document.getElementById("inventory").innerText =
data.products+" Active SKU";

}


if(document.getElementById("subscription")){

document.getElementById("subscription").innerText =
"ENTERPRISE Active Plan";

}


}catch(e){

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

