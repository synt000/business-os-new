from pathlib import Path

p = Path("src/static/js/dashboard_api.js")

s = p.read_text()

insert = r'''

// PREMIUM DASHBOARD METRICS
const widgets = data.widgets || {};

const revenueValue =
    today.today_revenue ||
    (widgets.sales && widgets.sales.today_revenue) ||
    0;

const ordersValue =
    today.today_orders ||
    (widgets.sales && widgets.sales.today_orders) ||
    0;

const customerValue =
    today.new_customers ||
    (widgets.customer && widgets.customer.total_customers) ||
    0;

const productValue =
    (widgets.inventory && widgets.inventory.total_products) ||
    0;


if(document.getElementById("revenue")){
    document.getElementById("revenue").innerText =
    Number(revenueValue).toLocaleString()+" MMK";
}

if(document.getElementById("orders")){
    document.getElementById("orders").innerText =
    ordersValue;
}

if(document.getElementById("customers")){
    document.getElementById("customers").innerText =
    customerValue;
}

if(document.getElementById("products")){
    document.getElementById("products").innerText =
    productValue;
}

'''

if "PREMIUM DASHBOARD METRICS" not in s:
    s += insert

p.write_text(s)

print("premium metrics patched")
