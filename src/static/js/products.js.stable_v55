const token = localStorage.getItem("access_token");


async function loadProducts(){

    const list = document.getElementById("list");

    try{

        const res = await fetch(
            "/api/v4/business/products",
            {
                headers:{
                    "Authorization":"Bearer " + token
                }
            }
        );


        const data = await res.json();

        console.log("PRODUCT DATA:", data);


        let html="";


        (data.products || []).forEach(p=>{

            html += `
            <div class="bg-gray-800 rounded-xl p-4">

                <h3 class="text-lg font-bold">
                📦 ${p.name}
                </h3>

                <p>
                SKU: ${p.sku || ""}
                </p>

                <p>
                Stock: ${p.stock_qty || 0}
                </p>

                <p>
                Buy: ${p.purchase_price || 0}
                </p>

                <p>
                Sell: ${p.retail_price || 0}
                </p>

            </div>
            `;

        });


        list.innerHTML =
        html || "No products found";


    }
    catch(e){

        console.error(e);

        list.innerHTML =
        "⚠️ Product loading failed";

    }

}



async function addProduct(){


    const body={

        sku:
        document.getElementById("sku").value,

        name:
        document.getElementById("name").value,

        barcode:
        document.getElementById("barcode").value,

        stock_qty:
        Number(document.getElementById("stock").value),

        purchase_price:
        Number(document.getElementById("purchase").value),

        retail_price:
        Number(document.getElementById("retail").value)

    };


    const res = await fetch(
        "/api/v4/business/products",
        {
            method:"POST",

            headers:{
                "Authorization":
                "Bearer " + token,

                "Content-Type":
                "application/json"
            },

            body:
            JSON.stringify(body)
        }
    );


    const result = await res.json();

    console.log(result);


    alert(
        "PRODUCT STATUS: " + res.status
    );


    loadProducts();

}



loadProducts();
