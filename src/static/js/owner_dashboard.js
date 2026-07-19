async function loadOwnerDashboard(){

    try{

        const token =
            localStorage.getItem("access_token") ||
            localStorage.getItem("token");

        if(!token){
            console.log("NO TOKEN");
            return;
        }


        const response = await fetch(
            "/owner/platform-summary",
            {
                headers:{
                    "Authorization":"Bearer " + token
                }
            }
        );


        const data = await response.json();

        console.log(
            "OWNER PLATFORM DATA:",
            data
        );


        if(data.status !== "SUCCESS"){
            return;
        }


        const platform = data.platform;


        const tenants =
            document.getElementById("tenants");

        const users =
            document.getElementById("users");

        const orders =
            document.getElementById("orders");

        const sales =
            document.getElementById("sales");


        if(tenants){
            tenants.innerText =
                platform.total_businesses ?? 0;
        }


        if(users){
            users.innerText =
                platform.total_users ?? 0;
        }


        if(orders){
            orders.innerText =
                platform.total_orders ?? 0;
        }


        if(sales){
            sales.innerText =
                "$" +
                Number(
                    platform.total_sales ?? 0
                ).toLocaleString();
        }


        console.log(
            "OWNER DASHBOARD UPDATED"
        );


    }
    catch(error){

        console.error(
            "OWNER DASHBOARD ERROR:",
            error
        );

    }

}



async function loadAdminPermissionPanel(){

    const list =
        document.getElementById("adminList");

    if(!list){
        return;
    }


    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const res = await fetch(
            "/admin/users",
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const admins =
            await res.json();


        if(!Array.isArray(admins)){

            list.innerText =
                "Admin Load Failed";

            return;
        }


        list.innerHTML =
            admins.map(
                admin => `

                <div class="admin-card">

                    <strong>
                    👤 ${admin.email}
                    </strong>

                    <br>

                    Role:
                    ${admin.role}

                    <br>

                    <button onclick="selectAdmin('${admin.id}')">
                    Select Admin
                    </button>

                </div>

                `
            ).join("");



    }
    catch(e){

        console.error(
            "ADMIN LOAD ERROR",
            e
        );

        list.innerText =
            "Admin Load Error";

    }

}






document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        loadOwnerDashboard();

        loadAdminPermissionPanel();

    }
);


// ================================
// ADMIN PERMISSION CHECKBOX UI
// ================================

let selectedAdminId = null;


async function selectAdmin(userId){

    selectedAdminId = userId;

    const panel =
        document.getElementById("permissionPanel");

    if(!panel){
        return;
    }

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const permRes = await fetch(
            "/permissions/all",
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const userPermRes = await fetch(
            `/admin/users/${userId}/permissions`,
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const allPermissions =
            await permRes.json();


        const userPermissions =
            await userPermRes.json();


        const current =
            (userPermissions.permissions || [])
            .map(
                p=>p.id
            );


        let groups = {};

        allPermissions.permissions.forEach(p=>{

            let module =
                p.code.split(".")[0];

            if(!groups[module]){
                groups[module] = [];
            }

            groups[module].push(p);

        });


        let html =
        "<h3>🔐 Permission Control</h3>";


        for(const module in groups){

            html += `
            <div class="permission-group">

            <h4>
            📁 ${module.toUpperCase()}
            </h4>
            `;


            groups[module].forEach(p=>{

                html += `
                <label>

                <input
                type="checkbox"
                ${current.includes(p.id) ? "checked":""}
                onchange="togglePermission('${userId}',${p.id},this)"
                >

                ${p.code}

                </label>
                <br>
                `;

            });


            html += `
            </div>
            <hr>
            `;

        }


        panel.innerHTML = html;


// ===============================
// PERMISSION HISTORY TIMELINE
// ===============================

const historyPanel =
    document.getElementById("permissionHistory");


if(historyPanel){

    const historyRes = await fetch(
        `/admin/users/${userId}/permission-history`,
        {
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    const historyData =
        await historyRes.json();


    historyPanel.innerHTML =
        (historyData.history || [])
        .map(
            h => `

            <div class="history-item">

            ${
                h.action === "GRANTED"
                ? "✅"
                : "❌"
            }

            ${
                h.action === "GRANTED"
                ? "🟢"
                : "🔴"
            }

            <strong>
            ${h.permission_code}
            </strong>

            <br>

            ${h.action}

            <br>

            <small>
            ${h.created_at}
            </small>

            </div>

            <hr>

            `
        )
        .join("")
        ||
        "No Activity";

}




    }
    catch(e){

        console.error(
            "PERMISSION UI ERROR",
            e
        );

        panel.innerText =
        "Permission Load Error";

    }

}



async function togglePermission(
    userId,
    permissionId,
    checkbox
){

    const checked = checkbox.checked;

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    const label =
        checked ? "Granting..." : "Removing...";


    showPermissionToast(label);


    try{

        const res = await fetch(
            `/admin/users/${userId}/permissions/${permissionId}`,
            {
                method:
                checked ? "POST" : "DELETE",

                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const data =
            await res.json();


        if(
            res.ok &&
            (
                data.status === "SUCCESS" ||
                data.status === "EXISTS"
            )
        ){

            showPermissionToast(
                checked
                ?
                "✅ Permission Granted"
                :
                "❌ Permission Removed"
            );

        }
        else{

            showPermissionToast(
                "⚠ Permission Update Failed"
            );

        }


    }
    catch(e){

        console.error(
            "Permission Update Error",
            e
        );


        checkbox.checked = !checked;

        showPermissionToast(
            "❌ Server Error"
        );

    }

}


function showPermissionToast(message){

    let toast =
        document.getElementById(
            "permissionToast"
        );


    if(!toast){

        toast =
        document.createElement(
            "div"
        );

        toast.id =
        "permissionToast";


        toast.style.position =
        "fixed";

        toast.style.bottom =
        "20px";

        toast.style.left =
        "50%";

        toast.style.transform =
        "translateX(-50%)";

        toast.style.background =
        "#111827";

        toast.style.color =
        "white";

        toast.style.padding =
        "12px 20px";

        toast.style.borderRadius =
        "12px";

        toast.style.zIndex =
        "9999";


        document.body.appendChild(
            toast
        );

    }


    toast.innerText =
    message;


    setTimeout(
        ()=>{
            toast.innerText="";
        },
        2000
    );

}



// =====================================
// AI BUSINESS INTELLIGENCE LOADER
// =====================================

async function loadAIInsights(){

    const panel = document.getElementById(
        "aiInsights"
    );

    if(!panel){
        return;
    }

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const res = await fetch(
            "/ai/insights",
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const data = await res.json();


        if(!Array.isArray(data)){
            panel.innerHTML =
            "⚠ AI data unavailable";
            return;
        }


        panel.innerHTML =
        data.map(item => `

            <div class="ai-card">

                <h4>
                🤖 ${item.title}
                </h4>

                <p>
                ${item.message}
                </p>

                <small>
                ${item.level}
                </small>

            </div>

        `).join("");

    }
    catch(e){

        console.error(
            "AI Insight Error",
            e
        );

        panel.innerHTML =
        "❌ AI Service Error";

    }

}


document.addEventListener(
    "DOMContentLoaded",
    loadAIInsights
);



// =====================================
// AI RECOMMENDATIONS LOADER
// =====================================

async function loadAIRecommendations(){

    const panel = document.getElementById(
        "aiRecommendations"
    );

    if(!panel){
        return;
    }


    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const res = await fetch(
            "/ai/recommendations",
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const data = await res.json();


        if(!Array.isArray(data)){

            panel.innerHTML =
            "⚠ No recommendations";

            return;
        }


        panel.innerHTML =
        data.map(item => {

            let icon = "🟢";

            if(item.priority === "HIGH"){
                icon = "🔴";
            }

            if(item.priority === "MEDIUM"){
                icon = "🟡";
            }

            return `

            <div class="ai-card">

                <h4>
                ${icon} ${item.title || "Recommendation"}
                </h4>

                <p>
                ${item.action || item.message || item}
                </p>

                <small>
                Priority: ${item.priority || "INFO"}
                </small>

            </div>

            `;

        }).join("");


    }
    catch(e){

        console.error(
            "AI Recommendation Error",
            e
        );

        panel.innerHTML =
        "❌ Recommendation Service Error";

    }

}


document.addEventListener(
    "DOMContentLoaded",
    loadAIRecommendations
);




// =====================================
// CEO DAILY BRIEF LOADER
// =====================================


async function loadCEOBrief(){

    const briefPanel =
        document.getElementById("ceoBrief");

    const scorePanel =
        document.getElementById("ceoScore");


    if(!briefPanel && !scorePanel){
        return;
    }


    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const briefRes = await fetch(
            "/ai/ceo-brief",
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const briefData =
            await briefRes.json();


        if(briefPanel){

            const insights =
                briefData.insights || [];


            const performance =
                briefData.performance || {};


            briefPanel.innerHTML = `

            <div class="ai-card">

                <h4>👑 CEO Performance</h4>

                <h2>
                ${performance.level || "ACTIVE"}
                </h2>


                <p>
                💰 Revenue:
                ${performance.revenue || 0}
                </p>


                <p>
                💎 Profit:
                ${performance.profit || 0}
                </p>


                <p>
                📈 Margin:
                ${performance.margin || 0}%
                </p>


            </div>


            <h4>
            🤖 AI Business Insights
            </h4>


            ${
                insights.map(item => `

                <div class="ai-card">

                    <h4>
                    🟢 ${item.title}
                    </h4>

                    <p>
                    ${item.message}
                    </p>

                    <small>
                    ${item.level}
                    </small>

                </div>

                `).join("")
            }


            `;

        }



        const scoreRes = await fetch(
            "/ai/ceo-score",
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const scoreData =
            await scoreRes.json();



        if(scorePanel){

            scorePanel.innerHTML = `


            <div class="ai-card">

                <h4>
                📊 Business Health Score
                </h4>


                <h1>
                ${scoreData.score || 0}
                /100
                </h1>


                <h3>
                ${scoreData.level || "UNKNOWN"}
                </h3>


                <hr>


                <p>
                📦 Inventory:
                ${scoreData.breakdown?.inventory_health || 0}
                </p>


                <p>
                💰 Cash Flow:
                ${scoreData.breakdown?.cash_flow || 0}
                </p>


                <p>
                📈 Sales:
                ${scoreData.breakdown?.sales_growth || 0}
                </p>


                <p>
                💎 Profit:
                ${scoreData.breakdown?.profit_health || 0}
                </p>


            </div>


            `;

        }


    }
    catch(e){

        console.error(
            "CEO AI Error",
            e
        );

    }

}


document.addEventListener(
    "DOMContentLoaded",
    loadCEOBrief
);


// =========================
// AI HISTORY TIMELINE
// =========================

async function loadAIHistory(){

    const panel = document.getElementById(
        "aiHistory"
    );

    if(!panel){
        return;
    }


    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const res = await fetch(
            "/ai/history",
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const data = await res.json();


        if(!Array.isArray(data)){
            panel.innerHTML =
            "❌ No AI History";
            return;
        }


        panel.innerHTML =
        data.map(item => {

            let icon = "🟢";

            if(item.priority === "WARNING"){
                icon = "🟡";
            }

            if(item.priority === "HIGH"){
                icon = "🔴";
            }


            return `
            <div class="ai-card">

                <h4>
                ${icon} ${item.title}
                </h4>

                <p>
                ${item.message}
                </p>

                <small>
                ${item.created_at}
                </small>

            </div>
            `;

        }).join("");


    }catch(e){

        console.error(
            "AI History Error",
            e
        );

        panel.innerHTML =
        "❌ AI History Error";

    }

}


document.addEventListener(
    "DOMContentLoaded",
    loadAIHistory
);









// =========================
// AI ACTION CENTER
// =========================

async function loadAIActions(){

    const panel = document.getElementById("aiActions");

    if(!panel){
        return;
    }

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const res = await fetch(
            "/ai/actions",
            {
                headers:{
                    "Authorization":
                    "Bearer " + token
                }
            }
        );


        const actions = await res.json();


        if(!Array.isArray(actions)){

            panel.innerHTML =
            "❌ No AI Actions";

            return;
        }


        panel.innerHTML =
        actions.map(item => `

        <div class="ai-card">

            <h4>
            🤖 ${item.title}
            </h4>


            <p>
            ${item.action}
            </p>


            <small>
            Priority:
            ${item.priority}
            </small>


            <br><br>


            <button
            onclick="executeAIAction('${item.action_id}')">

            Execute

            </button>


        </div>

        `).join("");



    }catch(error){

        console.error(
            "AI ACTION ERROR",
            error
        );

        panel.innerHTML =
        "❌ AI Action Error";

    }

}



async function executeAIAction(action_id){


    const token =
    localStorage.getItem("access_token") ||
    localStorage.getItem("token");



    const res = await fetch(

        `/ai/actions/${action_id}/execute`,

        {
            method:"POST",

            headers:{
                "Authorization":
                "Bearer " + token
            }
        }

    );


    const data =
    await res.json();


    alert(
        data.message ||
        "Action Completed"
    );


    loadAIActions();

}



document.addEventListener(
"DOMContentLoaded",
loadAIActions
);



async function loadAIProcurement(){

    const box = document.getElementById("aiProcurement");

    if(!box){
        return;
    }

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    try{

        const res = await fetch(
            "/ai/purchases/pending",
            {
                headers:{
                    "Authorization":"Bearer " + token
                }
            }
        );


        const data = await res.json();


        if(data.status !== "SUCCESS"){
            box.innerHTML =
            "AI Procurement Load Failed";
            return;
        }


        if(data.count === 0){

            box.innerHTML =
            `
            <div class="ai-empty">
            ✅ No Pending AI Purchase
            </div>
            `;

            return;
        }


        box.innerHTML =
        data.items.map(
            po => `

            <div class="ai-po-card">

            <h4>
            🛒 ${po.purchase_number}
            </h4>

            <div class="ai-po-status">
            ${
                po.status === "PENDING_APPROVAL"
                ? "🟡 Pending Approval"
                : po.status
            }
            </div>


            <p>
            💰 Amount:
            <strong>
            ${Number(po.amount).toLocaleString()} MMK
            </strong>
            </p>


            <div class="ai-timeline">

            <p>
            🟢 AI Purchase Created
            </p>

            <p>
            🟡 Waiting Owner Decision
            </p>

            <p>
            ⚪ Stock Receive Pending
            </p>

            </div>


            <div class="ai-po-actions">

            <button onclick="approveAIPO('${po.id}')">
            ✅ Approve
            </button>


            <button onclick="rejectAIPO('${po.id}')">
            ❌ Reject
            </button>

            </div>


            </div>

            `
        ).join("");

    }
    catch(e){

        console.error(
            "AI PROCUREMENT ERROR",
            e
        );

        box.innerHTML =
        "AI Procurement Error";

    }

}



async function approveAIPO(id){

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    await fetch(
        "/purchases/approve-ai-po/" + id,
        {
            method:"POST",
            headers:{
                "Authorization":"Bearer " + token
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
        "/ai/purchases/reject/" + id,
        {
            method:"POST",
            headers:{
                "Authorization":"Bearer " + token,
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



// ======================================
// ACTIVATION KEY GENERATOR
// ======================================

async function generateActivationKey(){

    const plan_id = document.getElementById("keyPlan").value;
    const duration_days = document.getElementById("keyDuration").value;

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    const res = await fetch(
        "/subscription/key/generate",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "Authorization":"Bearer " + token
            },
            body:JSON.stringify({
                plan_id: plan_id,
                duration_days: Number(duration_days)
            })
        }
    );


    const data = await res.json();


    if(res.ok){

        document.getElementById("generatedKey").innerHTML =
        `
        <div style="margin-top:15px;
        padding:15px;
        background:#0f172a;
        border-radius:10px;">
        ✅ KEY GENERATED
        <br><br>
        <b>${data.key_code || data.key}</b>
        </div>
        `;

    }else{

        document.getElementById("generatedKey").innerHTML =
        `
        ❌ ${JSON.stringify(data.detail)}
        `;

    }

}



// ======================================
// ACTIVATION KEY HISTORY
// ======================================

async function loadActivationKeys(){

    const box = document.getElementById("activationKeyHistory");

    if(!box){
        return;
    }

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    const res = await fetch(
        "/subscription/keys",
        {
            headers:{
                "Authorization":"Bearer " + token
            }
        }
    );


    const keys = await res.json();


    if(!res.ok){
        box.innerHTML = "❌ Failed loading keys";
        return;
    }


    if(keys.length === 0){
        box.innerHTML = "No activation keys";
        return;
    }


    box.innerHTML = keys.map(k => `

        <div style="
            margin-top:12px;
            padding:15px;
            background:#0f172a;
            border-radius:12px;
            border:1px solid #334155;
        ">

            🔑 <b>${k.key_code}</b>

            <br>

            📦 Plan:
            <span style="color:#38bdf8">
            ${k.plan_name}
            </span>

            <br>

            ⏳ Duration:
            ${k.duration_days} Days

            <br>

            ${
                k.status === "REVOKED"
                ?
                "⚫ REVOKED"
                :
                k.used
                ?
                "🔴 USED"
                :
                "🟢 AVAILABLE"
            }

            <br><br>

            <button
            onclick="copyActivationKey('${k.key_code}')"
            style="
                padding:10px 14px;
                border:none;
                border-radius:8px;
                background:#0284c7;
                color:white;
                cursor:pointer;
            ">
            📋 COPY KEY
            </button>

            ${
                k.status === "REVOKED"
                ?
                ""
                :
                `
                <button
                onclick="revokeActivationKey('${k.key_code}')"
                style="
                    margin-left:8px;
                    padding:10px 14px;
                    border:none;
                    border-radius:8px;
                    background:#dc2626;
                    color:white;
                ">
                ❌ REVOKE
                </button>
                `
            }

        </div>

    `).join("");

}



// Load after dashboard ready

document.addEventListener(
    "DOMContentLoaded",
    loadActivationKeys
);


// ======================================
// COPY ACTIVATION KEY
// ======================================

function copyActivationKey(key){

    navigator.clipboard.writeText(key)
    .then(()=>{

        alert(
            "✅ Copied: " + key
        );

    });

}



// ======================================
// REVOKE ACTIVATION KEY
// ======================================

async function revokeActivationKey(key){

    if(!confirm("Revoke " + key + " ?")){
        return;
    }

    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    const res = await fetch(
        "/subscription/key/revoke/" + key,
        {
            method:"POST",
            headers:{
                "Authorization":"Bearer " + token
            }
        }
    );


    const data = await res.json();


    if(res.ok){
        alert("✅ KEY REVOKED");
        loadActivationKeys();
    }
    else{
        alert(
            "❌ " + JSON.stringify(data.detail)
        );
    }

}



// ======================================
// ACTIVATION KEY MANAGEMENT V2
// ======================================

function activationStatusBadge(status){

    if(status === "AVAILABLE"){
        return `
        <span style="
            background:#166534;
            color:#86efac;
            padding:5px 10px;
            border-radius:20px;
            font-size:12px;
        ">
        🟢 AVAILABLE
        </span>`;
    }


    if(status === "USED"){
        return `
        <span style="
            background:#7f1d1d;
            color:#fca5a5;
            padding:5px 10px;
            border-radius:20px;
            font-size:12px;
        ">
        🔴 USED
        </span>`;
    }


    if(status === "REVOKED"){
        return `
        <span style="
            background:#334155;
            color:#cbd5e1;
            padding:5px 10px;
            border-radius:20px;
            font-size:12px;
        ">
        ⚫ REVOKED
        </span>`;
    }


    return status;

}



async function revokeActivationKey(key){

    if(!confirm(
        "Revoke this activation key?"
    )){
        return;
    }


    const token =
        localStorage.getItem("access_token") ||
        localStorage.getItem("token");


    const res = await fetch(
        `/subscription/key/revoke/${key}`,
        {
            method:"POST",
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    const data = await res.json();


    if(res.ok){

        alert(
            "✅ Key revoked"
        );

        loadActivationKeyHistory();

    }
    else{

        alert(
            JSON.stringify(data.detail)
        );

    }

}




function renderActivationKeys(keys){


    const box =
    document.getElementById(
        "activationKeyHistory"
    );


    if(!box){
        return;
    }


    box.innerHTML =
    keys.map(k => `


    <div style="
        margin-top:12px;
        padding:15px;
        background:#0f172a;
        border-radius:12px;
        border:1px solid #334155;
    ">


        🔑 <b>${k.key_code}</b>

        <br><br>


        📦 Plan:
        <span style="color:#38bdf8">
        ${k.plan_name}
        </span>


        <br>


        ⏳ ${k.duration_days} Days


        <br><br>


        ${activationStatusBadge(k.status)}


        <br><br>


        <button
        onclick="copyActivationKey('${k.key_code}')"
        style="
        padding:10px 14px;
        border-radius:8px;
        border:none;
        background:#2563eb;
        color:white;
        ">
        📋 COPY
        </button>


        ${
        k.status === "AVAILABLE"
        ?
        `
        <button
        onclick="revokeActivationKey('${k.key_code}')"
        style="
        margin-left:8px;
        padding:10px 14px;
        border-radius:8px;
        border:none;
        background:#dc2626;
        color:white;
        ">
        🚫 REVOKE
        </button>
        `
        :
        ""
        }


    </div>


    `).join("");

}



