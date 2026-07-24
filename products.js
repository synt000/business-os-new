


const token =
localStorage.getItem("access_token");



async function loadProducts(){

try{

console.log("LOAD PRODUCTS START");


let res =
await fetch(
"/api/v4/business/products",
{
headers:{
"Authorization":
"Bearer "+token
}
});


let data =
await res.json();

console.log("TOKEN:", token);
console.log("PRODUCT RESPONSE:", data);

console.log("PRODUCT COUNT:", data.products.length);

let total = data.products.length;


// PROFIT CALCULATION

let inventoryCost = 0;
let potentialRevenue = 0;

data.products.forEach(p=>{

    inventoryCost += 
    (p.purchase_price || 0) * (p.stock_qty || 0);

    potentialRevenue +=
    (p.retail_price || 0) * (p.stock_qty || 0);

});


let expectedProfit =
potentialRevenue - inventoryCost;


let profitMargin =
potentialRevenue
? ((expectedProfit / potentialRevenue) * 100).toFixed(2)
: 0;


document.getElementById("inventoryCost").innerText =
inventoryCost.toLocaleString()+" MMK";


document.getElementById("potentialRevenue").innerText =
potentialRevenue.toLocaleString()+" MMK";


document.getElementById("expectedProfit").innerText =
expectedProfit.toLocaleString()+" MMK";


document.getElementById("profitMargin").innerText =
profitMargin+" %";



let available = data.products.filter(
p=>p.stock_qty > 10
).length;

let low = data.products.filter(
p=>p.stock_qty > 0 && p.stock_qty <= (p.reorder_level || 5)
).length;

let out = data.products.filter(
p=>p.stock_qty === 0
).length;

let restock = data.products.filter(
p => p.need_restock === true
).length;

document.getElementById("restockProducts").innerText = restock;


document.getElementById("totalProducts").innerText = total;
document.getElementById("availableProducts").innerText = available;
document.getElementById("lowProducts").innerText = low;
document.getElementById("outProducts").innerText = out;



let search =
document.getElementById("search").value
.toLowerCase();



let html="";

let restockHTML = "";

data.products
.filter(p=>p.need_restock === true)
.forEach(p=>{

restockHTML += `
<div class="restock-item">
📦 ${p.name}<br>
SKU: ${p.sku}<br>
Current Stock: <b>${p.stock_qty}</b><br>
🔔 Reorder Level: <b>${p.reorder_level || 5}</b><br>
⚠️ Need: <b>${((p.reorder_level || 5) - p.stock_qty)} Units</b>
<br>
<button class="save" onclick="quickRestock('${p.id}',${((p.reorder_level || 5) - p.stock_qty)})">
➕ Restock ${((p.reorder_level || 5) - p.stock_qty)}
</button>
</div>
<hr>
`;

});

document.getElementById("restockList").innerHTML =
restockHTML || "✅ All stock levels OK";



data.products
.filter(p=>
p.name.toLowerCase()
.includes(search)
)
.forEach(p=>{


html += `

<div class="product">
<h3>📦 ${p.name}</h3>
<div class="badge">SKU: ${p.sku}</div>
<br>
<div class="${
p.stock_qty === 0
? 'stock-zero'
: p.stock_qty <= (p.reorder_level || 5)
? 'stock-low'
: 'stock-ok'
}">
📦 Stock: ${p.stock_qty}

${
p.stock_qty === 0
? " ❌ OUT OF STOCK"
: p.stock_qty <= (p.reorder_level || 5)
? " ⚠️ LOW STOCK"
: " ✅ AVAILABLE"
}

</div>

<button class="save" onclick="changeStock('${p.id}',1)">
➕ Stock
</button>

<button class="delete" onclick="changeStock('${p.id}',-1)">
➖ Stock
</button>

<br>
<div>🛒 Buy: <span class="price">${p.purchase_price}</span></div>
<br>
<div>💰 Sell: <span class="price">${p.retail_price}</span></div>

<br>

<div>
🔔 Reorder Level:
<span class="price">
${p.reorder_level || 5}
</span>
</div>

<div>
${
p.need_restock
?
`⚠️ Need Restock: ${((p.reorder_level || 5) - p.stock_qty)} Units`
:
`✅ Stock Level OK`
}
</div>

<br>


<div>
${p.purchase_price > 0 ? `
📊 Profit / Unit:
<span class="price">
${(p.retail_price-p.purchase_price).toLocaleString()} MMK
</span>

<br>

💵 Stock Profit:
<span class="price">
${((p.retail_price-p.purchase_price)*p.stock_qty).toLocaleString()} MMK
</span>

<br>

📈 Margin:
<span class="price">
${(((p.retail_price-p.purchase_price)/p.retail_price)*100).toFixed(2)}%
</span>

` : `

⚠️ Cost Missing

<br>

💵 Stock Profit:
<span class="price">
N/A
</span>

<br>

📈 Margin:
<span class="price">
N/A
</span>

`}
</div>

<br><br>
<button class="edit" onclick="editProduct('${p.id}','${p.name}',${p.retail_price})">
✏️ Edit
</button>
<button class="delete" onclick="deleteProduct('${p.id}')">
🗑 Delete
</button>


</div>


`;


});


if(html.trim() === ""){

html = `
<div class="text-center text-gray-500 py-10">
📦 No products found.<br>
Add your first product to start selling.
</div>
`;

}



document.getElementById("list")
.innerHTML=html;

}catch(err){

document.getElementById("list").innerHTML = `
<div class="text-center text-red-400 py-10">
⚠️ Unable to load products.<br>
Please try again.
</div>
`;

console.log(err);

}


}




async function addProduct(){

let token = localStorage.getItem("access_token");

if(!token){
    alert("LOGIN REQUIRED");
    return;
}





let body={


name: document.getElementById("name").value,


sku: document.getElementById("sku").value,


barcode: document.getElementById("barcode").value,


stock_qty:
Number(document.getElementById("stock").value),


purchase_price:
Number(document.getElementById("purchase").value),


retail_price:
Number(document.getElementById("retail").value)


};



let res = await fetch(
"/api/v4/business/products",
{

method:"POST",

headers:{
"Authorization":
"Bearer "+token,

"Content-Type":
"application/json"
},

body:
JSON.stringify(body)

});

let text = await res.text();

console.log("ADD RESPONSE:", res.status, text);

alert(res.status + "\n" + text);

loadProducts();
loadStockHistory();
loadInventorySummary();


}





let editId = null;


function editProduct(id,name,price){

editId = id;

document.getElementById("editName").value = name;
document.getElementById("editPrice").value = price;

document.getElementById("editModal").style.display="flex";

}


function closeEdit(){

document.getElementById("editModal").style.display="none";

}


async function saveEdit(){

let name =
document.getElementById("editName").value;

let price =
Number(document.getElementById("editPrice").value);


let res = await fetch(
"/api/v4/business/products/"+editId,
{
method:"PUT",
headers:{
"Authorization":"Bearer "+token,
"Content-Type":"application/json"
},
body:JSON.stringify({
name:name,
retail_price:price
})
});


let text = await res.text();

alert("UPDATE\n"+res.status+"\n"+text);

closeEdit();

loadProducts();

}


async function deleteProduct(id){


if(!confirm("Delete Product?"))
return;


await fetch(
"/api/v4/business/products/"+id,
{

method:"DELETE",

headers:{

"Authorization":
"Bearer "+token

}

});


loadProducts();


}



loadProducts();








async function quickRestock(id,qty){

let res = await fetch(
"/api/v4/business/products/"+id+"/stock",
{
method:"POST",
headers:{
"Authorization":"Bearer "+token,
"Content-Type":"application/json"
},
body:JSON.stringify({
quantity:qty,
reason:"Restock"
})
});

let data = await res.json();
console.log("RESTOCK:",data);

loadProducts();
loadStockHistory();
loadInventorySummary();

}


async function changeStock(id,amount){

let qty = prompt(
"📦 Enter Stock Quantity:",
"1"
);

if(qty===null) return;


let reason = prompt(
"📝 Reason:",
amount > 0 ? "Stock IN" : "Stock OUT"
);


let res = await fetch(
"/api/v4/business/products/"+id+"/stock",
{
method:"POST",
headers:{
"Authorization":"Bearer "+token,
"Content-Type":"application/json"
},
body:JSON.stringify({
quantity:Number(qty)*amount,
reason:reason
})
});


let text = await res.text();

alert(
"STOCK UPDATE\n"+
res.status+
"\n"+
text
);


loadProducts();

}





function formatDate(date){
    if(!date) return "";

    let d = new Date(date);

    return d.toLocaleString("en-GB",{
        day:"2-digit",
        month:"short",
        year:"numeric",
        hour:"2-digit",
        minute:"2-digit"
    });
}



async function loadInventorySummary(){

let res = await fetch(
"/api/v4/business/inventory-summary",
{
headers:{
"Authorization":"Bearer "+token
}
});

if(!res.ok) return;

let data = await res.json();

document.getElementById("totalUnits").innerText =
data.total_units;

document.getElementById("inventoryValue").innerText =
data.inventory_value.toLocaleString()+" MMK";

document.getElementById("inventoryQty").innerText =
data.total_products;

document.getElementById("avgValue").innerText =
data.total_products
? Math.round(data.inventory_value/data.total_products).toLocaleString()+" MMK"
: "0 MMK";

}



async function loadStockChart(){

let res = await fetch(
"/api/v4/business/stock-movements",
{
headers:{
"Authorization":"Bearer "+token
}
});

if(!res.ok) return;

let data = await res.json();
console.log("STOCK CHART DATA:", data);

let inQty = data
.filter(x=>x.movement_type==="IN")
.reduce((a,b)=>a+b.quantity_change,0);

let outQty = data
.filter(x=>x.movement_type==="OUT")
.reduce((a,b)=>a+Math.abs(b.quantity_change),0);


new Chart(
document.getElementById("stockChart"),
{
type:"bar",
data:{
labels:[
"🟢 IN",
"🔴 OUT"
],
datasets:[
{
label:"Stock Movement",
data:[
inQty,
outQty
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


async function loadStockHistory(){

let res = await fetch(
"/api/v4/business/stock-movements",
{
headers:{
"Authorization":"Bearer "+token
}
});

if(!res.ok) return;

let data = await res.json();

let html="";

data.forEach(m=>{

html += `
<tr>

<td>${formatDate(m.created_at)}</td>

<td>${m.product_name || m.product_id}</td>

<td>
${
m.movement_type==="IN"
?
'<span class="history-in">🟢 IN</span>'
:
'<span class="history-out">🔴 OUT</span>'
}
</td>

<td>
${
m.quantity_change > 0
?
`<span class="history-qty-in">+${m.quantity_change}</span>`
:
`<span class="history-qty-out">${m.quantity_change}</span>`
}
</td>

<td>${m.before_quantity}</td>

<td>${m.after_quantity}</td>
<td>${m.reason || ""}</td>

</tr>
`;

});


document.getElementById("history").innerHTML=html;

}



loadProducts();
loadStockHistory();
loadInventorySummary();

setTimeout(()=>{
    loadStockChart();
},500);

