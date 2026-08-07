async function loadRevenueExpenseChart(){

try{

const token = localStorage.getItem("access_token");

const res = await fetch(
"/api/v4/dashboard/summary",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


if(!res.ok){
console.error(
"Dashboard Summary Failed",
res.status
);
return;
}


const data = await res.json();

console.log(
"DASHBOARD SUMMARY CHART",
data
);


const summary = data.summary || data;



if(document.getElementById("chartRevenue")){
document.getElementById("chartRevenue").innerText =
(summary.revenue || 0).toLocaleString()+" MMK";
}


if(document.getElementById("chartExpense")){
document.getElementById("chartExpense").innerText =
(summary.expense || 0).toLocaleString()+" MMK";
}


if(document.getElementById("chartProfit")){
document.getElementById("chartProfit").innerText =
(summary.profit || 0).toLocaleString()+" MMK";
}


const margin =
summary.revenue > 0
?
((summary.profit / summary.revenue)*100).toFixed(1)
:
0;


if(document.getElementById("chartMargin")){
document.getElementById("chartMargin").innerText =
margin+"%";
}


const canvas =
document.getElementById(
"revenueExpenseChart"
);


if(!canvas){
console.error("CANVAS NOT FOUND");
return;
}


if(window.revenueExpenseChartInstance){
window.revenueExpenseChartInstance.destroy();
}


window.revenueExpenseChartInstance =
new Chart(
canvas,
{
type:"bar",

data:{
labels:[
"Revenue",
"Expense",
"Profit"
],

datasets:[
{
label:"MMK",

data:[
summary.revenue || 0,
summary.expense || 0,
summary.profit || 0
]
}
]
},

options:{
responsive:true,
maintainAspectRatio:false
}

}
);


console.log(
"FINANCE CHART READY"
);


}

catch(e){

console.error(
"CHART ERROR",
e
);

}

}



window.addEventListener(
"load",
loadRevenueExpenseChart
);

