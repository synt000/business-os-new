from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

if "loadProfitChart()" in text:
    print("✅ Profit JS Already Exists")
    raise SystemExit

js = '''

async function loadProfitChart(){

try{

const res = await fetch(
"/dashboard/revenue-expense",
{
headers:{
"Authorization":"Bearer "+localStorage.getItem("access_token")
}
}
);

const data = await res.json();

new Chart(
document.getElementById("profitChart"),
{
type:"line",
data:{
labels:["Revenue","Expense","Profit"],
datasets:[
{
label:"Business Performance",
data:[
data.summary.revenue,
data.summary.expense,
data.summary.profit
],
fill:false,
tension:0.35
}
]
},
options:{
responsive:true
}
}
);

}
catch(e){
console.log("Profit Chart Error",e);
}

}

loadProfitChart();

'''

text = text.replace("</script>", js + "\n</script>", 1)

p.write_text(text, encoding="utf-8")

print("✅ Profit JS Added")
