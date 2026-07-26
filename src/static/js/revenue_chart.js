async function loadRevenueExpenseChart(){

try{

const token = localStorage.getItem("access_token");
console.log("REVENUE TOKEN CHECK:", token);

const res = await fetch(
"/api/v4/owner/revenue-expense",
{
headers:{
"Authorization":"Bearer " + token
}
}
);


const data = await res.json();

console.log("FULL API DATA:",data);


const summary = data.summary || {};


document.getElementById("chartRevenue").innerText =
(summary.revenue || 0).toLocaleString()+" MMK";

document.getElementById("chartExpense").innerText =
(summary.expense || 0).toLocaleString()+" MMK";

document.getElementById("chartProfit").innerText =
(summary.profit || 0).toLocaleString()+" MMK";

const margin =
summary.revenue > 0
?
((summary.profit / summary.revenue)*100).toFixed(1)
:
0;

document.getElementById("chartMargin").innerText =
margin+"%";

console.log(
"PROFIT MARGIN:",
margin+"%"
);

// ================================





const canvas =
document.getElementById(
"revenueExpenseChart"
);


if(!canvas){
console.error("CANVAS NOT FOUND");
return;
}


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

datasets:[{

label:"MMK",

data:[
summary.revenue || 0,
summary.expense || 0,
summary.profit || 0
],

backgroundColor:[
"#00e676",
"#ff5252",
"#2196f3"
],

borderRadius:8

}]

},


options:{

responsive:true,
maintainAspectRatio:false,

animation:false,

scales:{

y:{

min:-15000,

max:25000,

ticks:{

autoSkip:false,

stepSize:5000

}

}

}

}

}

);


console.log("FINANCE CHART READY");


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



// ================================


