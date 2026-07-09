const API = "/api/v4";

function token() {
    return localStorage.getItem("access_token");
}

function authHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token()
    };
}

async function api(url, method = "GET", body = null) {
    const options = {
        method: method,
        headers: authHeaders()
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(API + url, options);

    if (response.status === 401) {
        localStorage.clear();
        window.location = "/login";
        return;
    }

    return await response.json();
}

async function login(email, password) {
    const response = await fetch(API + "/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok && data.access_token) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("role", data.role_profile);
        localStorage.setItem("workspace_id", data.workspace_id);

        window.location = "/dashboard";
    } else {
        alert(data.detail || "Login Failed");
    }
}

function logout() {
    localStorage.clear();
    window.location = "/login";
}

async function loadProducts() {
    const data = await api("/business/products");

    console.log("Products:", data);

    return data;
}
