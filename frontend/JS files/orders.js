document.addEventListener("DOMContentLoaded", async function () {
    const orderButton = document.getElementById("place-order-btn");
    const orderSummary = document.getElementById("order-summary");
    const API_BASE_URL = "https://newest-online-food-production-up.railway.app/api"; // Replace with your backend URL

    // 🔹 Function to load cart items from MongoDB
    async function loadOrderSummary() {
        try {
            const response = await fetch(`${API_BASE_URL}/cart`, {
                method: "GET",
                credentials: "include", // Ensure user authentication
            });

            if (!response.ok) {
                throw new Error("Failed to fetch cart data");
            }

            const cartItems = await response.json();
            orderSummary.innerHTML = "";

            if (cartItems.length === 0) {
                orderSummary.innerHTML = "<p>Your cart is empty.</p>";
                return;
            }

            cartItems.forEach(item => {
                const orderItem = document.createElement("div");
                orderItem.innerHTML = `
                    <h4>${item.name}</h4>
                    <p>Quantity: ${item.quantity}</p>
                    <p>Price: Ksh ${item.price * item.quantity}</p>
                `;
                orderSummary.appendChild(orderItem);
            });

        } catch (error) {
            console.error("Error loading order summary:", error);
        }
    }

    // 🔹 Function to place an order
    async function placeOrder() {
        try {
            const response = await fetch(`${API_BASE_URL}/orders`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include", // Ensure user authentication
            });

            if (!response.ok) {
                throw new Error("Failed to place order");
            }

            alert("Order placed successfully!");
            orderSummary.innerHTML = "<p>Order placed successfully! Your food is on the way.</p>";

            // Reload cart after placing order
            loadOrderSummary();

        } catch (error) {
            console.error("Error placing your order:", error);
            alert("Failed to place an order. Try again later.");
        }
    }

    // 🔹 Load order summary on page load
    await loadOrderSummary();

    // 🔹 Event listener for order button
    if (orderButton) {
        orderButton.addEventListener("click", placeOrder);
    }
});
