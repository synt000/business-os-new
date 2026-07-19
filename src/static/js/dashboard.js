async function loadCEOStats(){

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


try{

const res = await fetch(
"/ceo-summary",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


const data = await res.json();


console.log(
"CEO DASHBOARD",
data
);


if(data.status==="SUCCESS"){

const d=data.dashboard;


if(document.getElementById("revenue")){
document.getElementById("revenue").innerText =
Number(d.today_revenue).toLocaleString()+" MMK";
}


if(document.getElementById("orders")){
document.getElementById("orders").innerText =
d.today_orders;
}


if(document.getElementById("customers")){
document.getElementById("customers").innerText =
d.total_customers;
}


if(document.getElementById("products")){
document.getElementById("products").innerText =
d.total_products;
}


}


}catch(e){

console.error(
"CEO DASHBOARD ERROR",
e
);

}


}


document.addEventListener(
"DOMContentLoaded",
loadCEOStats
);


async function loadAIProcurement(){

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


const box = document.getElementById("aiPurchaseList");

if(!box) return;


try{

const res = await fetch(
"/ai/purchases/pending",
{
headers:{
"Authorization":"Bearer "+token
}
}
);


const data = await res.json();


if(
data.status==="SUCCESS" &&
data.items.length > 0
){

box.innerHTML = "";


data.items.forEach(po=>{


box.innerHTML += `

<div class="ai-po">

<div>
<b>${po.purchase_number}</b>
</div>

<div>
Amount:
${Number(po.amount).toLocaleString()} MMK
</div>

<div>
Status:
${po.status}
</div>


<button
class="ai-btn"
onclick="approveAIPO('${po.id}')">
✅ Approve
</button>


<button
class="ai-btn"
onclick="rejectAIPO('${po.id}')">
❌ Reject
</button>


</div>

`;


});


}else{


box.innerHTML =
"No Pending AI Purchase";


}


}catch(e){

console.error(
"AI PROCUREMENT ERROR",
e
);

box.innerHTML =
"AI Load Failed";

}


}



async function approveAIPO(id){

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


await fetch(
"/purchases/approve-ai-po/"+id,
{
method:"POST",
headers:{
"Authorization":"Bearer "+token
}
}
);


loadAIProcurement();

}



async function rejectAIPO(id){

const token =
localStorage.getItem("access_token") ||
localStorage.getItem("token");


await fetch(
"/ai/purchases/reject/"+id,
{
method:"POST",
headers:{
"Authorization":"Bearer "+token,
"Content-Type":"application/json"
},
body:JSON.stringify({
reason:"Rejected from Dashboard"
})
}
);


loadAIProcurement();

}



document.addEventListener(
"DOMContentLoaded",
loadAIProcurement
);

