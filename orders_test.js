
async function viewOrder(id){

const token = localStorage.getItem("access_token");

const res = await fetch(
"/api/v4/business/orders/detail/"+id,
{
headers:{
"Authorization":"Bearer "+token
}
}
);

const data = await res.json();

document.getElementById("orderDetail").innerHTML = `
<h3>${data.order_number}</h3>
<p>Customer: ${data.customer_name}</p>
<p>Status: ${data.status}</p>
<p>Total: ${data.total_amount}</p>

<h4>Items</h4>

${data.items.map(i=>`
<div>
${i.product_name} x ${i.quantity}
<br>
Price: ${i.price}
</div>
<hr>
`).join("")}

`;

document.getElementById("orderModal").style.display="flex";

}
function closeOrderModal(){
document.getElementById("orderModal").style.display="none";
}
