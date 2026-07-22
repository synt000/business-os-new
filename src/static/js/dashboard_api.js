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


