document.addEventListener("DOMContentLoaded", function () {
    const deliveryStatus = document.getElementById("delivery-status");
    const deliveryTime = document.getElementById("delivery-time");
    const trackButton = document.getElementById("track-delivery-btn");

    async function trackDelivery() {
        try {
            // Fetch user details from MongoDB
            const userResponse = await fetch("https://newest-online-food-production-up.railway.app/users/me", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            });

            if (!userResponse.ok) {
                throw new Error("Failed to fetch user data. Please log in again.");
            }

            const userData = await userResponse.json();
            const userId = userData._id; // Get MongoDB user ID

            // Fetch delivery status from MongoDB
            const response = await fetch(`https://newest-online-food-production-up.railway.app/delivery/status/${userId}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            });

            if (!response.ok) {
                throw new Error("Failed to fetch delivery status.");
            }

            const data = await response.json();

            if (data) {
                deliveryStatus.innerHTML = `Status: <b>${data.status}</b>`;
                deliveryTime.innerHTML = data.estimated_time 
                    ? `Estimated Time: <b>${data.estimated_time}</b>` 
                    : "Estimated time will be updated soon.";
            }
        } catch (error) {
            console.error("Error tracking delivery:", error);
            alert("Failed to track delivery. Please try again later.");
        }
    }

    if (trackButton) {
        trackButton.addEventListener("click", trackDelivery);
    }
});
