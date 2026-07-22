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


console.log(
"DASHBOARD WIDGET DATA",
data
);


const today=data.today || {};
const widgets=data.widgets || {};


function set(id,value){

const el=document.getElementById(id);

if(el){
el.innerText=value;
}

}


set(
"today-orders",
today.today_orders || 0
);


set(
"today-revenue",
Number(today.today_revenue || 0).toLocaleString()+" MMK"
);


set(
"new-customers",
today.new_customers || 0
);


set(
"low-stock",
today.low_stock || 0
);


set(
"social-leads",
today.social_leads || 0
);


set(
"notifications",
today.notifications || 0
);


// Revenue Chart

if(
window.Chart &&
data.sales_chart
){

const ctx =
document.getElementById(
"salesChart"
);


if(ctx){

new Chart(
ctx,
{
type:"line",

data:{
labels:
data.sales_chart.labels,

datasets:[
{
label:"Revenue",

data:
data.sales_chart.values,

borderWidth:3
}
]
},

options:{
responsive:true
}

}
);

}

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
