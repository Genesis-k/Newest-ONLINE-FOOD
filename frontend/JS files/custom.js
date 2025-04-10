document.addEventListener("DOMContentLoaded", async () => {
    await checkUserSession();
    setupEventListeners();
});

// Check if a user is logged in (Verify Session via Backend)
async function checkUserSession() {
    const token = localStorage.getItem("token");

    if (!token) {
        document.getElementById("loginBtn").style.display = "block";
        document.getElementById("logoutBtn").style.display = "none";
        return;
    }

    try {
        const response = await fetch("https://newest-online-food-production-up.railway.app/api/auth/me", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error("Session expired. Please log in again.");
        }

        const userData = await response.json();
        console.log("User session verified:", userData);

        document.getElementById("loginBtn").style.display = "none";
        document.getElementById("logoutBtn").style.display = "block";

    } catch (error) {
        console.error("User session check failed:", error);
        localStorage.removeItem("token"); // Remove invalid token
        document.getElementById("loginBtn").style.display = "block";
        document.getElementById("logoutBtn").style.display = "none";
    }
}

// Logout function (Clear Token and Redirect)
document.getElementById("logoutBtn").addEventListener("click", async () => {
    try {
        const response = await fetch("https://newest-online-food-production-up.railway.app/api/auth/logout", {
            method: "POST",
            headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
        });

        if (!response.ok) {
            throw new Error("Logout failed.");
        }

        localStorage.removeItem("token"); // Remove token
        window.location.href = "/login.html";
    } catch (error) {
        console.error("Error during logout:", error);
        alert("Failed to log out. Try again.");
    }
});

// Function to setup general event listeners
function setupEventListeners() {
    // Scroll to top button
    const scrollToTopBtn = document.getElementById("scrollToTopBtn");
    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
}
