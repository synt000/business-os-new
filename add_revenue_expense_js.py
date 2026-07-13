from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

if "loadRevenueExpense()" in text:
    print("✅ Revenue Expense JS already exists")
    raise SystemExit

js = '''

async function loadRevenueExpense(){

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
document.getElementById("revenueExpenseChart"),
{
type:"bar",
data:{
labels:["Revenue","Expense","Profit"],
datasets:[
{
label:"Amount",
data:[
data.summary.revenue,
data.summary.expense,
data.summary.profit
]
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
console.log("Revenue Expense Error",e);
}

}

loadRevenueExpense();

'''

text = text.replace("</script>", js + "\n</script>", 1)

p.write_text(text, encoding="utf-8")

print("✅ Revenue Expense JS Added")
