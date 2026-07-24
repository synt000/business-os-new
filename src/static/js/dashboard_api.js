console.log("DASHBOARD_API_LOADED");

async function loadDashboardWidgets(){

console.log("STEP 1");


// Dashboard Loading State
const loadingTargets = [
    "heroSales",
    "heroOrders",
    "heroGrowth",
    "revenue",
    "orders",
    "customers",
    "products"
];


loadingTargets.forEach(id => {

    const el = document.getElementById(id);

    if(el){

        el.innerText = "Loading...";

    }

});


try{

const token = localStorage.getItem("access_token");

console.log("TOKEN =", token);

const res = await fetch(
"/api/v4/dashboard/summary",
{
headers:{
"Authorization":"Bearer "+token
}
}
);

console.log("STATUS =", res.status);

if(!res.ok){

    console.error(
        "Dashboard API failed:",
        res.status
    );


    if(res.status === 401){

        localStorage.removeItem("access_token");
        localStorage.removeItem("tenant_id");


        alert(
            "🔐 Session expired. Please login again."
        );


        window.location.href = "/login";

        return;

    }


    const errorBox = document.getElementById(
        "dashboard-error"
    );

    if(errorBox){

        errorBox.style.display = "block";

        errorBox.innerText =
        "⚠️ Dashboard temporarily unavailable. Please try again.";

    }

    return;
}

const data = await res.json();

console.log("SUMMARY DATA =", data);

const d = data.dashboard || data;

console.log("D =", d);


// FINANCE KPI BINDING

if(document.getElementById("total_invoice")){
    document.getElementById("total_invoice").innerText =
    d.total_invoice || 0;
}

if(document.getElementById("paid_invoice")){
    document.getElementById("paid_invoice").innerText =
    d.paid_invoice || 0;
}

if(document.getElementById("total_payment")){
    document.getElementById("total_payment").innerText =
    (d.total_payment || 0).toLocaleString();
}

if(document.getElementById("receivable_balance")){
    document.getElementById("receivable_balance").innerText =
    (d.receivable_balance || 0).toLocaleString();
}

console.log("FINANCE KPI LOADED", {
    invoice:d.total_invoice,
    paid:d.paid_invoice,
    payment:d.total_payment,
    receivable:d.receivable_balance
});


// AI FINANCE INSIGHT

try{

const financeRes = await fetch(
    "/owner/finance-insight",
    {
        headers:{
            "Authorization":"Bearer "+token
        }
    }
);

if(financeRes.ok){

    const financeData = await financeRes.json();

    const finance = financeData.ai_finance || {};

    if(document.getElementById("finance_health")){
        document.getElementById("finance_health").innerText =
        (finance.finance_health || 0) + "%";
    }


    if(document.getElementById("estimated_profit")){
        document.getElementById("estimated_profit").innerText =
        (finance.estimated_profit || 0).toLocaleString() + " MMK";
    }


    if(document.getElementById("finance_advice")){

        let advice = "Business analysis complete.";

        if((finance.estimated_profit || 0) < 0){
            advice = "⚠️ Expense is higher than revenue. Review purchase cost.";
        }

        else{
            advice = "✅ Business finance is healthy.";
        }

        document.getElementById("finance_advice").innerText = advice;
    }


    

// ================================
// AI FINANCE EXPLANATION ENGINE
// ================================

if(document.getElementById("finance_score")){

let score = finance.finance_health || 0;

document.getElementById("finance_score").innerText =
score + " / 100";


let explanation = "";

if(score >= 80){

explanation =
"🚀 Strong business position. Focus on growth and customer expansion.";

}

else if(score >= 50){

explanation =
"⚠️ Business is stable. Monitor expenses and improve cash flow.";

}

else{

explanation =
"🔴 Attention needed. Review sales, expenses and debts.";

}


document.getElementById("finance_explanation").innerText =
explanation;


}




// ================================
// AI CEO INTELLIGENCE ENGINE
// ================================

if(document.getElementById("ceo_advice")){

let profit = finance.estimated_profit || 0;
let revenue = finance.revenue || 0;


let advice="";


if(profit > 0 && revenue > 0){

advice =
"🚀 Sales are positive. Increase marketing and customer acquisition.";

}

else if(revenue > 0){

advice =
"⚠️ Revenue detected. Monitor expenses carefully.";

}

else{

advice =
"🔴 Need more sales activity.";

}


document.getElementById("ceo_advice").innerText =
advice;



let forecast =
"Expected revenue growth opportunity.";

if(profit > 0){

forecast =
"📈 Positive cash flow expected if sales continue.";

}
else{

forecast =
"⚠️ Cash pressure possible. Review expenses.";

}


document.getElementById("cash_forecast").innerText =
forecast;



let risk =
"No critical risk detected.";

if(revenue === 0){

risk =
"⚠️ No revenue activity.";

}

else if(profit < 0){

risk =
"🔴 Loss risk detected.";

}


document.getElementById("ai_risk_monitor").innerText =
risk;


}




// ================================
// AI INVENTORY INTELLIGENCE
// ================================


if(document.getElementById("inventory_status")){


let orders =
d.today_orders || 0;


let inventoryMessage="";


if(orders > 5){

inventoryMessage =
"⚠️ Sales velocity high. Monitor stock levels.";

}

else{

inventoryMessage =
"✅ Stock level appears stable.";

}


document.getElementById("inventory_status")
.innerText =
inventoryMessage;



let restock =
"✅ No urgent purchase needed.";


if(orders > 5){

restock =
"🛒 Recommended: Prepare restock for fast moving products.";

}


document.getElementById("restock_advice")
.innerText =
restock;



let productAI =
"📦 Waiting for product sales data.";


if(orders > 0){

productAI =
"🏆 Best sellers detected. Consider increasing inventory.";

}


document.getElementById("top_product_ai")
.innerText =
productAI;



}




// ================================
// AI SALES & CUSTOMER INTELLIGENCE
// ================================


if(document.getElementById("customer_ai")){


let customers =
d.customers || 0;

let orders =
d.today_orders || 0;


let customerMsg =
"👥 Customer activity is stable.";


if(customers > 0){

customerMsg =
"👥 Existing customers detected. Focus on retention.";

}


document.getElementById("customer_ai")
.innerText =
customerMsg;



let forecast =
"📊 Waiting for more sales data.";


if(orders > 0){

forecast =
"📈 Sales trend is positive. Growth opportunity detected.";

}


document.getElementById("sales_forecast")
.innerText =
forecast;



let marketing =
"🎯 Improve product visibility and customer engagement.";


if(orders > 0){

marketing =
"🚀 Promote best-selling products to increase revenue.";

}


document.getElementById("marketing_ai")
.innerText =
marketing;



let productGrowth =
"🏆 Product performance data collecting.";


if(orders > 0){

productGrowth =
"🥇 Fast moving products should receive priority stock.";

}


document.getElementById("product_growth_ai")
.innerText =
productGrowth;


}


console.log("AI FINANCE LOADED", finance);

}

}catch(err){

console.error("AI FINANCE ERROR", err);

}



console.log("heroSales =", document.getElementById("heroSales"));

if(document.getElementById("heroSales")){
document.getElementById("heroSales").innerText =
(d.today_revenue || 0).toLocaleString() + " MMK";
}

if(document.getElementById("heroOrders")){
document.getElementById("heroOrders").innerText =
d.today_orders || 0;
}


if(document.getElementById("heroGrowth")){

let growth =
d.trends?.growth_label || "0%";

const heroGrowthEl = document.getElementById("heroGrowth");

if(heroGrowthEl){

const rg = Number(d.trends?.revenue_growth ?? 0);

let title = "";

if(rg >= 100){
    title = "🚀 Exceptional Growth";
}
else if(rg > 20){
    title = "📈 Strong Growth";
}
else if(rg > 0){
    title = "↗ Growing";
}
else if(rg < 0){
    title = "📉 Declining";
}
else{
    title = "Stable";
}

heroGrowthEl.innerText =
(d.trends?.growth_label || "0%") + " " + title;

}

}


if(document.getElementById("growth-rate")){
    document.getElementById("growth-rate").innerText =
        (d.trends?.growth_label || "0%") + " Growth";
}


if(document.getElementById("revenue")){
document.getElementById("revenue").innerText =
(d.today_revenue || 0).toLocaleString() + " MMK";
}

if(document.getElementById("orders")){
document.getElementById("orders").innerText =
d.today_orders || 0;
}

if(document.getElementById("order-growth")){
    const og = Number(d.trends?.orders_growth ?? 0);

    let label = "0%";

    if(og > 0){
        label = "↑ " + og + "%";
    }
    else if(og < 0){
        label = "↓ " + Math.abs(og) + "%";
    }

    const orderGrowthEl = document.getElementById("order-growth");

if(orderGrowthEl){
    if(og > 0){
        orderGrowthEl.innerText =
            "↑ " + og + "% vs yesterday";
        orderGrowthEl.className = "stat-growth positive";
    }
    else if(og < 0){
        orderGrowthEl.innerText =
            "↓ " + Math.abs(og) + "% vs yesterday";
        orderGrowthEl.className = "stat-growth negative";
    }
    else{
        orderGrowthEl.innerText =
            "0% Today";
        orderGrowthEl.className = "stat-growth neutral";
    }
}
}

if(document.getElementById("customers")){
document.getElementById("customers").innerText =
d.total_customers || 0;
}

if(document.getElementById("customer-growth")){

    const cg = Number(d.trends?.customer_growth ?? 0);

    let label = "0%";

    if(cg > 0){
        label = "↑ " + cg + "%";
    }
    else if(cg < 0){
        label = "↓ " + Math.abs(cg) + "%";
    }

    const customerGrowthEl = document.getElementById("customer-growth");

if(customerGrowthEl){
    if(cg > 0){
        customerGrowthEl.innerText =
            "↑ " + cg + "% New";
        customerGrowthEl.className = "stat-growth positive";
    }
    else{
        customerGrowthEl.innerText =
            "No new customers today";
        customerGrowthEl.className = "stat-growth neutral";
    }
}
}

if(document.getElementById("products")){
document.getElementById("products").innerText =
d.total_products || 0;
}


/* AI PROCUREMENT ENGINE */

if(document.getElementById("aiPurchaseList")){

const lowStock = Number(d.low_stock ?? 0);

if(lowStock > 0){

document.getElementById("aiPurchaseList").innerHTML = `
<div class="ai-po">
<b>⚠ Purchase Recommendation</b>
<br>
${lowStock} items need restock
<br>
<button class="ai-btn">
Create Purchase
</button>
</div>
`;

}
else{

document.getElementById("aiPurchaseList").innerHTML = `
<div class="ai-po">
<b>✅ Stock Healthy</b>
<br>
No purchase needed
</div>
`;

}

}


if(document.getElementById("product-growth")){

const pg = Number(d.low_stock ?? 0);

let label = "Stock Ready";

if(pg > 0){
    label = "⚠ " + pg + " Low Stock";
}

document.getElementById("product-growth").innerText =
label;

}

/* REVENUE TREND CHART */

if(
    window.Chart &&
    d.sales_chart
){

    const ctx =
        document.getElementById("salesChart");

    if(ctx){

        const gradient = ctx.getContext("2d").createLinearGradient(
            0,0,0,300
        );

        gradient.addColorStop(0,"rgba(0,229,255,0.45)");
        gradient.addColorStop(1,"rgba(0,229,255,0.02)");

        Chart.register(ChartDataLabels);

        new Chart(
            ctx,
            {
                type:"line",

                data:{
                    labels:d.sales_chart.labels.map(function(date){
                            const d = new Date(date);

                            if(isNaN(d)){
                                return date;
                            }

                            return d.toLocaleDateString(
                                "en-US",
                                {
                                    day:"numeric",
                                    month:"short"
                                }
                            );
                        }),

                    datasets:[
                                    {
                                        label:"Revenue (MMK)",
                                        data:d.sales_chart.revenue,
                                        borderWidth:3,
                                        borderColor:"#00e5ff",
                                        backgroundColor:gradient,
                                        fill:true,
                                        tension:0.45,
                                        pointRadius:5,
                                        pointHoverRadius:8,

                                        datalabels:{
                                            display:true,
                                            color:"#ffffff",
                                            anchor:"end",
                                            align:"top",
                                            font:{
                                                size:12,
                                                weight:"bold"
                                            },
                                            formatter:function(value){
                                                return Number(value).toLocaleString()+" MMK";
                                            }
                                        }
                                    },
                                    {
                                        label:"Orders",
                                        data:d.sales_chart.orders,
                                        borderWidth:2,
                                        borderColor:"#ffcc00",
                                        backgroundColor:"transparent",
                                        fill:false,
                                        tension:0.45,
                                        pointRadius:4,
                                        pointHoverRadius:7,

                                        datalabels:{
                                            display:true,
                                            color:"#ffcc00",
                                            anchor:"end",
                                            align:"bottom",
                                            font:{
                                                size:11,
                                                weight:"bold"
                                            },
                                            formatter:function(value){
                                                return value + " Orders";
                                            }
                                        }
                                    }
                                ]
                },

                  options:{
                      responsive:true,
                      maintainAspectRatio:false,

                      layout:{
                          padding:{
                              top:20,
                              right:16,
                              bottom:10,
                              left:16
                          }
                      },

                      animation:{
                          duration:1200
                      },

                      interaction:{
                          mode:"index",
                          intersect:false
                      },

                      scales:{
                          x:{
                              grid:{
                                  color:"rgba(148,163,184,0.12)"
                              },
                              ticks:{
                                  color:"#A3AED0"
                              }
                          },
                          y:{
                              grid:{
                                  color:"rgba(148,163,184,0.12)"
                              },
                              ticks:{
                                  color:"#A3AED0",
                                  callback:function(value){
                                      return Number(value).toLocaleString();
                                  }
                              }
                          }
                      },

                      plugins:{
                          legend:{
                              display:true,
                              labels:{
                                  color:"#E5E7EB"
                              }
                          },
                          tooltip:{
                              backgroundColor:"#111827",
                              titleColor:"#ffffff",
                              bodyColor:"#E5E7EB"
                          }
                      }
                  }
            }
        );

    }

}


console.log("STEP END");

}catch(e){

console.error("DASHBOARD ERROR =",e);

}

}

document.addEventListener(
"DOMContentLoaded",
loadDashboardWidgets
);


console.log("FINAL TEST LOADED");


// ===============================
// REVENUE EXPENSE KPI BINDING
// ===============================

async function loadRevenueExpense(){

    try{

        const token = localStorage.getItem("access_token");

        const res = await fetch(
            "/owner/revenue-expense",
            {
                headers:{
                    "Authorization":"Bearer " + token
                }
            }
        );


        if(!res.ok){
            console.error(
                "Revenue Expense API Failed",
                res.status
            );
            return;
        }


        const data = await res.json();

        console.log(
            "REVENUE EXPENSE DATA",
            data
        );


        const summary = data.summary || {};


        if(document.getElementById("total_revenue")){
            document.getElementById("total_revenue").innerText =
            (summary.revenue || 0).toLocaleString() + " MMK";
        }


        if(document.getElementById("total_expense")){
            document.getElementById("total_expense").innerText =
            (summary.expense || 0).toLocaleString() + " MMK";
        }


        if(document.getElementById("total_profit")){
            document.getElementById("total_profit").innerText =
            (summary.profit || 0).toLocaleString() + " MMK";
        }


    }catch(e){

        console.error(
            "REVENUE EXPENSE ERROR",
            e
        );

    }

}


document.addEventListener(
"DOMContentLoaded",
loadRevenueExpense
);


console.log(
"REVENUE EXPENSE BINDING LOADED"
);



// ================================
// AI FINANCE INSIGHT BINDING
// ================================

async function loadFinanceInsight(){

try{

const token = localStorage.getItem("access_token");


const res = await fetch(
"/owner/finance-insight",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


if(!res.ok){

console.error(
"FINANCE INSIGHT API FAILED",
res.status
);

return;

}


const data = await res.json();


console.log(
"FINANCE INSIGHT DATA",
data
);


const finance = data.ai_finance || {};


if(document.getElementById("finance_health")){

document.getElementById("finance_health").innerText =
(finance.finance_health || 0) + "%";

}


if(document.getElementById("estimated_profit")){

document.getElementById("estimated_profit").innerText =
(finance.estimated_profit || 0).toLocaleString()
+ " MMK";

}


if(document.getElementById("finance_advice")){


let advice="";


if(finance.estimated_profit < 0){

advice =
"⚠️ Expense is higher than revenue. Review purchase cost.";

}else{

advice =
finance.ai_action || "✅ Business profit is healthy.";

}


document.getElementById("finance_advice").innerText =
finance.ai_action || advice;


if(document.getElementById("finance_margin")){
    document.getElementById("finance_margin").innerText =
    (finance.margin || 0) + "%";
}


if(document.getElementById("finance_status")){
    const statusEl = document.getElementById("finance_status");

    statusEl.innerText =
    finance.status || "Unknown";

    statusEl.className = "finance-badge";

    if(finance.status === "Healthy"){
        statusEl.classList.add("finance-healthy");
    }
    else if(finance.status === "Warning"){
        statusEl.classList.add("finance-warning");
    }
    else{
        statusEl.classList.add("finance-danger");
    }
}


if(document.getElementById("finance_risk")){
    document.getElementById("finance_risk").innerText =
    finance.risk || "No data";
}


if(document.getElementById("finance_action")){
    const actionEl = document.getElementById("finance_action");

    actionEl.innerText =
    finance.ai_action || "No action";

    actionEl.className = "finance-action-box";
}


}


}catch(e){

console.error(
"FINANCE INSIGHT ERROR",
e
);

}


}



document.addEventListener(
"DOMContentLoaded",
loadFinanceInsight
);


console.log(
"AI FINANCE INSIGHT BINDING LOADED"
);



// ================================
// REVENUE EXPENSE CHART BINDING
// ================================

async function loadRevenueExpenseChart(){

try{

const token = localStorage.getItem("access_token");


const res = await fetch(
"/owner/revenue-expense",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


const data = await res.json();

console.log(
"REVENUE EXPENSE CHART DATA",
data
);


const summary = data.summary || {};


const canvas =
document.getElementById(
"revenueExpenseChart"
);


if(canvas){


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
]

}]

},


options:{
    responsive:true,
    maintainAspectRatio:false,

    layout:{
        padding:{
            top:20,
            right:20,
            bottom:10,
            left:10
        }
    },

    interaction:{
        mode:"index",
        intersect:false
    },

    plugins:{
        legend:{
            display:true,
            labels:{
                color:"#A3AED0",
                font:{
                    size:12,
                    weight:"600"
                }
            }
        },

        tooltip:{
            backgroundColor:"#111827",
            titleColor:"#ffffff",
            bodyColor:"#A3AED0",
            borderColor:"#334155",
            borderWidth:1,
            padding:12
        }
    },

    scales:{
        x:{
            grid:{
                display:true,
                color:"rgba(148,163,184,0.12)"
            },
            ticks:{
                color:"#A3AED0"
            }
        },

        y:{
            grid:{
                color:"rgba(148,163,184,0.12)"
            },
            ticks:{
                color:"#A3AED0",
                callback:function(value){
                    return Number(value).toLocaleString()+" MMK";
                }
            }
        }
    },


}

}

);


}


}catch(e){

console.error(
"REVENUE EXPENSE CHART ERROR",
e
);

}


}


document.addEventListener(
"DOMContentLoaded",
loadRevenueExpenseChart
);


console.log(
"REVENUE EXPENSE CHART LOADED"
);



// =====================================
// REVENUE EXPENSE CHART BINDING
// =====================================

async function loadRevenueExpenseChart(){

try{

const token = localStorage.getItem("access_token");

const res = await fetch(
"/owner/revenue-expense",
{
headers:{
"Authorization":"Bearer " + token
}
}
);


if(!res.ok){
console.error(
"Revenue Expense Chart API Failed",
res.status
);
return;
}


const data = await res.json();

console.log(
"REVENUE EXPENSE CHART DATA",
data
);


const summary = data.summary || {};


const canvas =
document.getElementById(
"revenueExpenseChart"
);


if(!canvas){
console.error(
"Chart canvas missing"
);
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

]

}]

},

options:{

responsive:true,

plugins:{

legend:{
display:false
}

}

}

}

);


}catch(e){

console.error(
"REVENUE EXPENSE CHART ERROR",
e
);

}

}


document.addEventListener(
"DOMContentLoaded",
loadRevenueExpenseChart
);


console.log(
"REVENUE EXPENSE CHART BINDING LOADED"
);



// =================================
// REVENUE EXPENSE CHART BINDING
// =================================

async function loadRevenueExpenseChart(){

try{

const res = await fetch(
"/owner/revenue-expense"
);

if(!res.ok){
console.error(
"Revenue Expense Chart API Failed",
res.status
);
return;
}


const data = await res.json();

console.log(
"CHART DATA",
data
);


const summary = data.summary || {};


const canvas =
document.getElementById(
"revenueExpenseChart"
);


if(!canvas){
console.log(
"Chart canvas not found"
);
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

]

}]

},

options:{

responsive:true,

plugins:{

legend:{
display:false
}

}

}

}

);


}catch(e){

console.error(
"REVENUE EXPENSE CHART ERROR",
e
);

}

}


document.addEventListener(
"DOMContentLoaded",
loadRevenueExpenseChart
);


console.log(
"REVENUE EXPENSE CHART LOADED"
);



// ================================
// AI CEO REPORT GENERATOR v7
// ================================

function generateCEOReport(){


let revenue = 760;
let orders = 1;


if(typeof d !== "undefined"){

    revenue = d.today_revenue || revenue;
    orders = d.today_orders || orders;

}


const report =

`
👋 Good Morning Owner

📊 Today's Business Summary

💰 Revenue:
${revenue.toLocaleString()} MMK


📦 Orders:
${orders}


🧠 AI Analysis:

Business performance is positive.

Main Recommendation:

🚀 Increase marketing
🚀 Focus on customer retention
🚀 Maintain stock availability
`;


const reportEl =
document.getElementById(
"ai_daily_report"
);


if(reportEl){

reportEl.innerText = report;

}



const alertEl =
document.getElementById(
"ai_alerts"
);


if(alertEl){

alertEl.innerText =

`
✅ No critical risk detected.

📦 Inventory stable.

💰 Cash position healthy.
`;

}



const decisionEl =
document.getElementById(
"ai_decision"
);


if(decisionEl){

decisionEl.innerText =

`
1️⃣ Promote best-selling products

2️⃣ Increase customer engagement

3️⃣ Prepare growth campaign
`;

}


console.log(
"AI CEO REPORT GENERATED"
);


}


window.addEventListener(
"load",
generateCEOReport
);



// ======================================
// AI DECISION CENTER v8
// ======================================

async function loadAIDecision(){

try{

const token = localStorage.getItem("access_token");


const res = await fetch(
    "/owner/ai-decision",
    {
        headers:{
            "Authorization":"Bearer "+token
        }
    }
);


if(!res.ok){

console.error(
"AI DECISION API FAILED",
res.status
);

return;

}


const data = await res.json();


const ai = data.ai_decision || {};


const box = document.getElementById(
    "ai_decision"
);


if(box){


box.innerHTML = `

🟢 Business Status:
<br>
<strong>${ai.business_status || "UNKNOWN"}</strong>

<br><br>

🚀 Recommendation:
<br>
${ai.ai_recommendation || "-"}

<br><br>

📅 Cash Flow Forecast:
<br>
${ai.cashflow_forecast || "-"}

<br><br>

🎯 Next Actions:
<br>
${(ai.next_action || []).join("<br>")}

`;

}


console.log(
"AI DECISION LOADED",
ai
);


}
catch(err){

console.error(
"AI DECISION ERROR",
err
);

}

}


loadAIDecision();



// ======================================
// AI GROWTH PLAN BUTTON ENGINE
// ======================================

document.addEventListener(
"DOMContentLoaded",
()=>{


const growthBtn =
document.getElementById(
"growth_plan_btn"
);


if(growthBtn){


growthBtn.addEventListener(
"click",
async ()=>{


try{


const token =
localStorage.getItem(
"access_token"
);



const res =
await fetch(
"/owner/growth-plan",
{
headers:{
"Authorization":
"Bearer "+token
}
}
);



const data =
await res.json();



const plan =
data.growth_plan;


let box =
document.getElementById(
"growth_plan_content"
);


if(!box){
console.log("Growth Plan container missing");
return;
}


let html =
`
<div style="
background:#111827;
color:white;
padding:20px;
border-radius:18px;
margin:10px 0;
">

<h2>🚀 AI Growth Plan</h2>

<p>
<b>Status:</b>
${plan.status}
</p>

<hr>

<h3>📌 Business Summary</h3>

<p>
${plan.summary}
</p>

<hr>

<h3>📅 Weekly Action Plan</h3>

`;

plan.weekly_plan.forEach(
w=>{

html +=
`
<div style="
background:#1f2937;
padding:12px;
margin:8px 0;
border-radius:10px;
">

<b>${w.week}</b>

<br>

${w.action}

</div>
`;

});

html +=
`
</div>
`;

box.innerHTML=html;

}
catch(e){

console.log(
"Growth Plan Error",
e
);

}

}
);

}
});



// ======================================
// AI EXECUTIVE DASHBOARD V4
// ======================================

async function loadAIExecutiveDashboard(){

try{

const ai = await apiFetch("/owner/ai-dashboard");

let aiBox = document.getElementById("aiExecutiveDashboard");

if(!aiBox){

aiBox = document.createElement("div");
aiBox.id="aiExecutiveDashboard";

aiBox.style.marginTop="20px";

document.body.appendChild(aiBox);

}


const d = ai.executive_dashboard;


aiBox.innerHTML = `

<div style="
background:#111827;
color:white;
padding:20px;
border-radius:18px;
margin-top:20px;
">

<h2>
🤖 AI CEO Executive Dashboard
</h2>


<h3>
Business Health:
${d.business_health.score}/100
</h3>

<p>
Status:
<b>${d.business_health.status}</b>
</p>


<hr>


<h3>
💰 Revenue Intelligence
</h3>

<p>
Current:
<b>${d.revenue.current}</b>
</p>

<p>
Forecast:
<b>${d.revenue.forecast}</b>
</p>


<hr>


<h3>
🏆 Top Product
</h3>

<p>
${d.top_product.name}
</p>

<p>
Units Sold:
${d.top_product.units_sold}
</p>


<hr>


<h3>
👥 Customer Intelligence
</h3>

<p>
Retention:
${d.customer.retention.score}
</p>

<p>
${d.customer.retention.status}
</p>


<hr>


<h3>
🚀 CEO Decision
</h3>

<p>
${d.final_decision}
</p>


</div>

`;

}catch(e){

console.log(
"AI Executive Dashboard Error",
e
);

}







}

loadAIExecutiveDashboard();




// ======================================
// CEO REPORT POPUP ENGINE
// ======================================


function closeCEOReport(){

let modal =
document.getElementById(
"ceo_modal"
);

if(modal)
modal.style.display="none";

}



document.addEventListener(
"DOMContentLoaded",
()=>{


let btn =
document.getElementById(
"ceo_report_btn"
);



if(btn){


btn.onclick=async()=>{


let modal =
document.getElementById(
"ceo_modal"
);


let box =
document.getElementById(
"ceo_content"
);


modal.style.display="block";



try{


let res =
await fetch(
"/owner/ceo-report",
{
headers:{
"Authorization":
"Bearer "+
localStorage.getItem(
"access_token"
)
}
}
);



let data =
await res.json();


let r =
data.ceo_report;



let html =
`
${r.greeting}

<br><br>

📊 Business Summary

<br>

💰 Revenue:
${r.kpi.revenue}

<br>

🛒 Orders:
${r.kpi.orders}

<br>

📦 Inventory:
${r.inventory_ai.warning}

<br><br>

🧠 AI Analysis:

<br>
${r.business_health.status}

<br><br>

🎯 CEO Strategy:

<br>
`;



r.ai_strategy.forEach(
x=>{

html +=
x+
"<br>";

}
);



html +=
`
<br>
🏆 CEO Decision:

<br>
${r.ceo_decision}
`;



box.innerHTML=html;


// ======================================
// AI EXECUTIVE DASHBOARD V4
// ======================================

try{

const ai = await apiFetch("/owner/ai-dashboard");

let aiBox = document.getElementById("aiExecutiveDashboard");

if(!aiBox){

aiBox = document.createElement("div");
aiBox.id="aiExecutiveDashboard";

aiBox.style.marginTop="20px";

document.body.appendChild(aiBox);

}


const d = ai.executive_dashboard;


aiBox.innerHTML = `

<div style="
background:#111827;
color:white;
padding:20px;
border-radius:18px;
margin-top:20px;
">

<h2>
🤖 AI CEO Executive Dashboard
</h2>


<h3>
Business Health:
${d.business_health.score}/100
</h3>

<p>
Status:
<b>${d.business_health.status}</b>
</p>


<hr>


<h3>
💰 Revenue Intelligence
</h3>

<p>
Current:
<b>${d.revenue.current}</b>
</p>

<p>
Forecast:
<b>${d.revenue.forecast}</b>
</p>


<hr>


<h3>
🏆 Top Product
</h3>

<p>
${d.top_product.name}
</p>

<p>
Units Sold:
${d.top_product.units_sold}
</p>


<hr>


<h3>
👥 Customer Intelligence
</h3>

<p>
Retention:
${d.customer.retention.score}
</p>

<p>
${d.customer.retention.status}
</p>


<hr>


<h3>
🚀 CEO Decision
</h3>

<p>
${d.final_decision}
</p>


</div>

`;

}catch(e){

console.log(
"AI Executive Dashboard Error",
e
);

}




}catch(e){

box.innerHTML=
"❌ CEO Report Error";

}


};


}


});
// ======================================
// SMART RESTOCK POPUP ENGINE
// ======================================

function closeRestockModal(){

let modal =
document.getElementById(
"restock_modal"
);

if(modal){
modal.style.display="none";
}

}

document.addEventListener(
"DOMContentLoaded",
()=>{

let btn =
document.getElementById(
"smart_restock_btn"
);

if(btn){

btn.onclick = async()=>{

let modal =
document.getElementById(
"restock_modal"
);

let box =
document.getElementById(
"restock_content"
);

modal.style.display="block";

try{

let res =
await fetch(
"/owner/smart-restock",
{
headers:{
"Authorization":
"Bearer "+
localStorage.getItem("access_token")
}
}
);

let data =
await res.json();

let ai =
data.smart_restock;

let html =
`
📦 Inventory Health:
<br>
${ai.inventory_health}

<br><br>
`;

ai.recommendations.forEach(
r=>{

html +=
`
🏆 Product:
${r.product}

<br>

📉 Current Stock:
${r.current_stock}

<br>

📦 Recommendation:
${r.recommended_purchase}

<br>

💡 Reason:
${r.reason}

<br><br>
`;

});

html +=
"🤖 " + ai.ai_message;

box.innerHTML=html;

}catch(e){

box.innerHTML="❌ Smart Restock Error";

}

};

}

});

