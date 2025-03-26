const API_BASE_URL = "https://your-railway-app-url/api";

async function login(event) {
    event.preventDefault();
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "foods.html"; // Redirect to food menu
    } else {
        alert(data.detail);
    }
}

async function register(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
        alert("Registration successful! You can now log in.");
        window.location.href = "login.html";
    } else {
        alert(data.detail);
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}
