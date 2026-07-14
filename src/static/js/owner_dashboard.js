// OWNER DASHBOARD JS V2
async function loadOwnerDashboard(){

    try {

        const response = await fetch("/platform/dashboard", {
            headers:{
                "Authorization": "Bearer " + (localStorage.getItem("access_token") || localStorage.getItem("token"))
            }
        });

        const data = await response.json();
        console.log("OWNER API DATA", data);

        if(data.status !== "SUCCESS"){
            console.log(data);
            return;
        }


        const dashboard = data.dashboard;
        const owner = data.owner_dashboard || dashboard.owner_dashboard;
        const stats = dashboard.statistics;

        console.log("STAT DEBUG", stats);


        document.getElementById("ownerEmail").innerText =
            data.owner || "Owner";


        document.getElementById("tenants").innerText =
            stats.tenants;


        document.getElementById("users").innerText =
            stats.users;


        document.getElementById("orders").innerText =
            stats.orders;


        document.getElementById("sales").innerText =
            stats.sales.toLocaleString();


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
                loadPermissions(admin.role);
            };


            box.appendChild(btn);

        }

    });

}



async function loadPermissions(role){

    const token =
    localStorage.getItem("access_token")
    || localStorage.getItem("token");


    const res = await fetch(
        "/permissions/role/" + role,
        {
            headers:{
                "Authorization":
                "Bearer " + token
            }
        }
    );


    const data =
    await res.json();


    const panel =
    document.getElementById(
        "permissionPanel"
    );


    panel.innerHTML =
    "<h3>"+role+" Permissions</h3>";


    const groups = {};


    data.permissions.forEach(p=>{

        const module =
        p.module || "general";


        if(!groups[module]){
            groups[module]=[];
        }


        groups[module].push(p);

    });


    Object.keys(groups).forEach(module=>{


        panel.innerHTML +=
        `
        <h4>
        📂 ${module.toUpperCase()}
        </h4>
        `;


        groups[module].forEach(p=>{


            panel.innerHTML +=
            `
            <label>

            <input
            type="checkbox"
            class="permission-check"
            data-id="${p.id}"
            checked>

            ${p.code}

            </label>
            `;

        });

    });


    panel.innerHTML +=
    `
    <button
    id="selectAllBtn">
    ☑ SELECT ALL
    </button>

    <button
    id="clearAllBtn">
    ☐ CLEAR ALL
    </button>

    <button
    id="savePermissionBtn">
    💾 SAVE CHANGES
    </button>
    `;


    document
    .getElementById("selectAllBtn")
    .onclick=()=>{

        document
        .querySelectorAll(".permission-check")
        .forEach(c=>c.checked=true);

    };


    document
    .getElementById("clearAllBtn")
    .onclick=()=>{

        document
        .querySelectorAll(".permission-check")
        .forEach(c=>c.checked=false);

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


// ===== OWNER PERMISSION PANEL INIT =====


async function loadAdminPermissionPanel(){

    const token =
    localStorage.getItem("access_token")
    || localStorage.getItem("token");


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


    const box =
    document.getElementById("adminList");


    box.innerHTML="";


    admins.forEach(admin=>{


        if(admin.role !== "OWNER"){


            const btn =
            document.createElement("button");


            btn.innerText =
            admin.full_name +
            " ("+
            admin.role+
            ")";


            btn.onclick = ()=>{

                selectedAdmin = admin;

                loadPermissions(
                    admin.role
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

    loadAdminPermissionPanel();

});


// FORCE OWNER DASHBOARD INIT
setTimeout(()=>{
    console.log("OWNER DASHBOARD FORCE START");
    loadOwnerDashboard();

    if(typeof loadAdminPermissionPanel === "function"){
        loadAdminPermissionPanel();
    }

},500);

