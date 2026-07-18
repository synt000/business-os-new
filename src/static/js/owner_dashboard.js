// OWNER DASHBOARD JS V2
async function loadOwnerDashboard(){

    try {

        const response = await fetch("/platform/dashboard", {
            headers:{
                "Authorization": "Bearer " + (localStorage.getItem("access_token") || localStorage.getItem("token"))
            }
        });

        const data = await response.json();
alert(JSON.stringify(data));
        console.log("OWNER API DATA", data);

        if(data.status !== "SUCCESS"){
            console.log(data);
            return;
        }


        const dashboard = data.dashboard;
        const owner = data.owner_dashboard || dashboard.owner_dashboard;
        const stats = dashboard.statistics;

        console.log("STAT DEBUG", stats);


//         document.getElementById("ownerEmail").innerText =
//             data.owner || "Owner";


//         document.getElementById("tenants").innerText =
//             stats.tenants;


//         document.getElementById("users").innerText =
//             stats.users;


        document.getElementById("orders").innerText =
            stats.orders;


//         document.getElementById("sales").innerText =
//             stats.sales.toLocaleString();


        if(document.getElementById("employees")){
            document.getElementById("employees").innerText =
                owner.employees;
        }


        if(document.getElementById("growth")){
            document.getElementById("growth").innerText =
                owner.growth_percent + "%";
        }


        if(document.getElementById("aiRequests")){
            document.getElementById("aiRequests").innerText =
                owner.ai_requests;
        }


        if(document.getElementById("topBusiness")){
            document.getElementById("topBusiness").innerText =
                owner.top_business;
        }


        console.log("OWNER DASHBOARD LOADED", data);


    } catch(error){

        console.error(
            "Dashboard Error:",
            error
        );

    }

}


loadOwnerDashboard();


// ================================
// ADMIN PERMISSION MANAGEMENT
// ================================

let selectedAdmin = null;


async function loadAdmins(){

    const token = localStorage.getItem("access_token");

try {
    const res = await fetch(
        "/admin/users",
        {
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    const admins = await res.json();
} catch(e) {
console.error(e);
return;
}


    const box =
    document.getElementById(
        "adminList"
    );


    box.innerHTML = "";


    admins.forEach(admin=>{

        if(admin.role !== "OWNER"){

            const btn =
            document.createElement(
                "button"
            );

            btn.innerHTML =
            admin.full_name +
            " ("+
            admin.role+
            ")";


            btn.onclick = ()=>{
                selectedAdmin = admin;
                loadUserPermissions(admin.id);
            };


            box.appendChild(btn);

        }

    });

}






// ======================================
// USER PERSONAL PERMISSION PANEL
// ======================================


async function loadUserPermissions(userId){

    selectedAdmin = {
        id:userId
    };


    const token =
    localStorage.getItem("access_token")
    || localStorage.getItem("token");


    const allRes = await fetch(
        "/permissions/all",
        {
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    const allData = await allRes.json();


    const userRes = await fetch(
        "/admin/users/" + userId + "/permissions",
        {
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    const userData = await userRes.json();


    const current =
    new Set(
        userData.permissions.map(
            p=>p.id
        )
    );


    const panel =
    document.getElementById(
        "permissionPanel"
    );


    panel.innerHTML =
    `
    <h3>🔐 Personal Permissions</h3>
    `;


    allData.permissions.forEach(p=>{


        panel.innerHTML +=
        `
        <label>

        <input
        type="checkbox"
        class="user-permission-check"
        data-id="${p.id}"
        ${current.has(p.id) ? "checked":""}
        >

        ${p.code}

        </label>
        `;


    });


    panel.innerHTML +=
    `
    <button id="saveUserPermissionBtn">
    💾 SAVE PERSONAL PERMISSIONS
    </button>
    `;


    document
    .getElementById(
        "saveUserPermissionBtn"
    )
    .onclick = async()=>{


        const checks =
        document.querySelectorAll(
            ".user-permission-check"
        );


        for(
            const check of checks
        ){

            const id =
            check.dataset.id;


            if(check.checked){

                await fetch(
                "/admin/users/"
                + userId
                + "/permissions/"
                + id,
                {
                    method:"POST",
                    headers:{
                    "Authorization":
                    "Bearer "+token
                    }
                });

            }
            else{

                await fetch(
                "/admin/users/"
                + userId
                + "/permissions/"
                + id,
                {
                    method:"DELETE",
                    headers:{
                    "Authorization":
                    "Bearer "+token
                    }
                });

            }

        }


        alert(
        "✅ Personal Permissions Saved"
        );


    };

}

async function loadPermissions(role){

    const token =
    localStorage.getItem("access_token")
    || localStorage.getItem("token");


try {
    const res = await fetch(
        "/permissions/role/" + role,
        {
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    const data = await res.json();


    const panel =
    document.getElementById(
        "permissionPanel"
    );


    if(!data.permissions){

        panel.innerHTML =
        "<h3>No Permissions Found</h3>";

        return;
    }


    panel.innerHTML =
    `
    <h3>
    🔐 ${role} Permissions
    </h3>
    `;


    const groups = {};


    data.permissions.forEach(p=>{

        const module =
        (p.module || "general")
        .toUpperCase();


        if(!groups[module]){
            groups[module]=[];
        }


        groups[module].push(p);

    });


    Object.keys(groups)
    .sort()
    .forEach(module=>{


        panel.innerHTML +=
        `
        <div class="permission-group">

        <h4>
        📂 ${module}
        </h4>
        `;


        groups[module]
        .sort((a,b)=>
            a.code.localeCompare(b.code)
        )
        .forEach(p=>{


            panel.innerHTML +=
            `
            <label class="permission-item">

            <input
            type="checkbox"
            class="permission-check"
            data-id="${p.id}"
            checked>

            <span>
            ${p.code}
            </span>

            </label>
            `;


        });


        panel.innerHTML +=
        `
        </div>
        `;


    });


    panel.innerHTML +=
    `
    <div class="permission-actions">

    <button id="selectAllBtn">
    ☑ SELECT ALL
    </button>

    <button id="clearAllBtn">
    ☐ CLEAR ALL
    </button>

    <button id="savePermissionBtn">
    💾 SAVE CHANGES
    </button>

    </div>
    `;


    document
    .getElementById("selectAllBtn")
    .onclick=()=>{

        document
        .querySelectorAll(".permission-check")
        .forEach(
            c=>c.checked=true
        );

    };


    document
    .getElementById("clearAllBtn")
    .onclick=()=>{

        document
        .querySelectorAll(".permission-check")
        .forEach(
            c=>c.checked=false
        );

    };


    document
    .getElementById("savePermissionBtn")
    .onclick =
    savePermissions;


}


async function savePermissions(){

    if(!selectedAdmin){

        alert(
            "Select Admin First"
        );

        return;

    }


    const token =
    localStorage.getItem(
        "access_token"
    );


    const checks =
    document.querySelectorAll(
        ".permission-check"
    );


    for(
        const check of checks
    ){

        const permissionId =
        Number(
            check.dataset.id
        );


        const roleName =
        selectedAdmin.role;


        if(check.checked){

            await fetch(
                "/permissions/assign",
                {
                    method:"POST",

                    headers:{
                        "Authorization":
                        "Bearer " + token,

                        "Content-Type":
                        "application/json"
                    },

                    body:JSON.stringify({
                        role_name:
                        roleName,

                        permission_id:
                        permissionId
                    })
                }
            );


        } else {


            await fetch(
                "/permissions/remove",
                {
                    method:"DELETE",

                    headers:{
                        "Authorization":
                        "Bearer " + token,

                        "Content-Type":
                        "application/json"
                    },

                    body:JSON.stringify({

                        role_name:
                        roleName,

                        permission_id:
                        permissionId

                    })

                }
            );


        }

    }


    alert(
        "✅ Permissions Saved"
    );

}




// ================================
// ROLE SELECTOR UI
// ================================

function loadRoleSelector(){

    const box =
    document.getElementById(
        "roleSelector"
    );

    if(!box) return;


    box.innerHTML = `

    <h3>🎭 Role Management</h3>

    <button class="role-btn" data-role="OWNER">
    👑 OWNER
    </button>

    <button class="role-btn" data-role="ADMIN">
    👨‍💼 ADMIN
    </button>

    <button class="role-btn" data-role="STAFF">
    👤 STAFF
    </button>

    <button class="role-btn" data-role="CASHIER">
    💰 CASHIER
    </button>

    `;


    document
    .querySelectorAll(".role-btn")
    .forEach(btn=>{

        btn.onclick = ()=>{

            const role =
            btn.dataset.role;


            loadPermissions(role);

        };

    });

}


// ===== OWNER PERMISSION PANEL INIT =====



async function loadAdminPermissionPanel(roleFilter=null){

    const token =
    localStorage.getItem("access_token")
    || localStorage.getItem("token");


try {
    const res = await fetch(
        "/admin/users",
        {
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    const admins = await res.json();
} catch(e) {
console.error(e);
return;
}


    const box =
    document.getElementById("adminList");


    box.innerHTML="";


    admins.forEach(admin=>{


        if(admin.role !== "OWNER"){

            if(roleFilter && admin.role !== roleFilter){
                return;
            }


            const btn =
            document.createElement("button");


            btn.innerText =
            admin.full_name +
            " ("+
            admin.role+
            ")";


            btn.onclick = ()=>{

                selectedAdmin = admin;

                loadUserPermissions(
                    admin.id
                );

            };


            box.appendChild(btn);

        }

    });


}







document.addEventListener(
"DOMContentLoaded",
()=>{

    loadOwnerDashboard();

    loadRoleSelector();
    loadAdminPermissionPanel();

});



document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
        console.log("No access token found.");
        return;
    }

    try {
        const res = await fetch("/platform/dashboard", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        console.log("Dashboard API:", data);

        if (data.status !== "SUCCESS") return;

        const dashboard = data.dashboard.owner_dashboard;

        const revenue = document.getElementById("revenue");
        const orders = document.getElementById("orders");
        const businesses = document.getElementById("businesses");
        const employees = document.getElementById("employees");

        if (revenue) revenue.textContent = dashboard.monthly_revenue;
        if (orders) orders.textContent = dashboard.orders;
        if (businesses) businesses.textContent = dashboard.active_businesses;
        if (employees) employees.textContent = dashboard.employees;

    } catch (err) {
        console.error("Dashboard Load Error:", err);
    }
});


document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    try {
        const res = await fetch("/platform/dashboard", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();
        if (data.status !== "SUCCESS") return;

        const owner = data.dashboard.owner_dashboard;
        const stats = data.dashboard.statistics;

        document.getElementById("revenue").textContent =
            owner.monthly_revenue.toLocaleString();

        document.getElementById("orders").textContent =
            owner.orders;

        document.getElementById("customers").textContent =
            stats.customers;

        document.getElementById("products").textContent =
            stats.products;

    } catch (e) {
        console.error("Dashboard API Error:", e);
    }
});
