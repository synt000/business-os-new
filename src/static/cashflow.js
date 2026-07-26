async function loadCashflow(){

    const token = localStorage.getItem("access_token");

    const res = await fetch(
        "/api/v4/owner/cashflow",
        {
            headers:{
                "Authorization":"Bearer "+token
            }
        }
    );

    const data = await res.json();

    document.getElementById("totalRevenue").innerText =
        data.total_revenue.toLocaleString();

    document.getElementById("totalCollected").innerText =
        data.total_collected.toLocaleString();

    document.getElementById("pendingReceivable").innerText =
        data.pending_receivable.toLocaleString();

    document.getElementById("cashAmount").innerText =
        data.payment_methods.CASH || 0;

    document.getElementById("waveAmount").innerText =
        data.payment_methods.WAVE || 0;
}


window.addEventListener(
    "load",
    loadCashflow
);
