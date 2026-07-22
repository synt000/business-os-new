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



// ===============================
// Dynamic Business Widget Renderer
// ===============================

const grid = document.getElementById(
    "dynamic-widget-grid"
);

if(grid && widgets){

    grid.innerHTML = "";

    Object.entries(widgets).forEach(
        ([key,value])=>{

            let title =
                key
                .replaceAll("_"," ")
                .replace(/\b\w/g,
                c=>c.toUpperCase()
                );


            let display = "";

            if(typeof value === "object"){

                if(value.status){
                    display=value.status;
                }
                else if(value.items){
                    display =
                    value.items.length +
                    " items";
                }
                else if(value.amount !== undefined){
                    display =
                    Number(value.amount)
                    .toLocaleString()
                    +" MMK";
                }
                else if(value.revenue !== undefined){
                    display =
                    Number(value.revenue)
                    .toLocaleString()
                    +" MMK";
                }
                else if(value.count !== undefined){
                    display=value.count;
                }
                else{
                    display="READY";
                }

            }else{

                display=value;

            }


            grid.innerHTML += `

            <div class="widget-card">

            <h3>
            ${title}
            </h3>

            <strong>
            ${display}
            </strong>

            </div>

            `;


        }
    );

}



}



// ===============================
// Dynamic Revenue Trend Chart
// ===============================

if(
    window.Chart &&
    document.getElementById("salesChart") &&
    data.sales_chart
){

    const chartData=data.sales_chart;


    const ctx =
    document
    .getElementById("salesChart")
    .getContext("2d");


    if(window.salesTrendChart){
        window.salesTrendChart.destroy();
    }


    window.salesTrendChart =
    new Chart(ctx,{

        type:"line",

        data:{

            labels:
            chartData.labels || [],

            datasets:[{

                label:"Revenue MMK",

                data:
                chartData.values || [],


                borderWidth:3,

                tension:0.4,

                fill:true

            }]

        },


        options:{

            responsive:true,

            plugins:{

                legend:{
                    display:true
                }

            },

            scales:{

                y:{
                    beginAtZero:true
                }

            }

        }

    });

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
