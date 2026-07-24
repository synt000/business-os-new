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

                    animation:{
                        duration:1200
                    },

                    plugins:{
                        legend:{
                            display:true
                        },

                        tooltip:{
                            callbacks:{
                                label:function(context){

                                    const value = Number(
                                        context.raw || 0
                                    ).toLocaleString();

                                    if(context.dataset.label === "Orders"){
                                        return value + " Orders";
                                    }

                                    return value + " MMK";

                                }
                            }
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
