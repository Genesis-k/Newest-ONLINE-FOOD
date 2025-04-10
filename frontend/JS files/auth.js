const API_BASE_URL = "https://newest-online-food-production-up.railway.app/api/auth"; // Replace with actual backend URL

document.addEventListener("DOMContentLoaded", () => {
    setupAuthEventListeners();
});

// Setup event listeners for login and register forms
function setupAuthEventListeners() {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            await loginUser();
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            await registerUser();
        });
    }
}

// Login function
async function loginUser() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            // Store JWT token
            localStorage.setItem("token", data.access_token);

            // Fetch user details from MongoDB
            const userResponse = await fetch(`${API_BASE_URL}/me`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${data.access_token}`
                }
            });

            if (!userResponse.ok) {
                throw new Error("Failed to fetch user details.");
            }

            const userData = await userResponse.json();

            // Store user ID from MongoDB for later API requests
            sessionStorage.setItem("user_id", userData._id); 

            alert("Login successful");
            window.location.href = "/frontpage.html";
        } else {
            alert(data.detail || "Login Failed");
        }
    } catch (error) {
        console.error("Error Logging in", error);
        alert("An error occurred. Please try again.");
    }
}

// Register Function
async function registerUser() {
    const username = document.getElementById("registerUsername").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;

    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Registration successful! You can now log in.");
            window.location.href = "/login.html";
        } else {
            alert(data.detail || "Registration Failed");
        }
    } catch (error) {
        console.error("Error Registering user", error);
        alert("An error occurred while registering. Please try again.");
    }
}

// Logout function
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("token"); // Clear authentication token
    sessionStorage.removeItem("user_id"); // Remove stored user ID
    window.location.href = "/login.html";
});
