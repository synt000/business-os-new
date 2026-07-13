from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

if "loadSalesTrend()" in text:
    print("✅ Sales Trend JS already exists")
    raise SystemExit

js = '''

async function loadSalesTrend(){

try{

const res = await fetch(
"/dashboard/sales-trend",
{
headers:{
"Authorization":"Bearer "+localStorage.getItem("access_token")
}
}
);

const data = await res.json();

const labels = data.trend.map(x=>x.date);
const sales = data.trend.map(x=>x.sales);

new Chart(
document.getElementById("salesChart"),
{
type:"line",
data:{
labels:labels,
datasets:[
{
label:"Sales",
data:sales,
fill:false,
tension:0.35
}
]
},
options:{
responsive:true,
plugins:{
legend:{
display:true
}
}
}
}
);

}
catch(e){
console.log("Sales Trend Error",e);
}

}

loadSalesTrend();

'''

text = text.replace("</script>", js + "\n</script>", 1)

p.write_text(text, encoding="utf-8")

print("✅ Sales Trend JS Added")

