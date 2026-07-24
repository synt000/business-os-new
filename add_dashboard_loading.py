from pathlib import Path

p = Path("src/static/js/dashboard_api.js")

s = p.read_text()

old = '''console.log("STEP 1");

try{

const token = localStorage.getItem("access_token");'''

new = '''console.log("STEP 1");


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

const token = localStorage.getItem("access_token");'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ Dashboard loading state added")
else:
    print("❌ start block not found")
