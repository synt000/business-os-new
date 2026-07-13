from pathlib import Path

p=Path("src/templates/orders.html")
t=p.read_text()

old='''async function updateOrderStatus(id,status){'''

new='''async function updateOrderStatus(id,status){

const token = localStorage.getItem("access_token");

'''

t=t.replace(old,new)

p.write_text(t)

print("ORDERS TOKEN FIXED")
