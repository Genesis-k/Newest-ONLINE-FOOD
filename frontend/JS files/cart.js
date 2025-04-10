const cartContainer = document.getElementById("cart-items");
const totalPriceElement = document.getElementById("total-price");

const API_BASE_URL = "https://newest-online-food-production-up.railway.app/api"; // Change this to your actual backend URL

// 🔹 Load cart from MongoDB
async function loadCart() {
    try {
        const response = await fetch(`${API_BASE_URL}/cart`, {
            method: "GET",
            credentials: "include",  // Ensures user authentication
        });

        if (!response.ok) {
            throw new Error("Failed to fetch cart data");
        }

        const cart = await response.json();
        cartContainer.innerHTML = "";

        if (cart.length === 0) {
            cartContainer.innerHTML = "<p>Your cart is empty</p>";
            totalPriceElement.textContent = "Ksh 0";
            return;
        }

        let total = 0;
        cart.forEach((item) => {
            total += item.price * item.quantity;

            const cartItem = document.createElement("div");
            cartItem.classList.add("cart-item");

            cartItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <h3>${item.name}</h3>
                <p>Price: Ksh ${item.price}</p>
                <p>Quantity:
                    <button onclick="updateQuantity('${item._id}', -1)">-</button>
                    ${item.quantity}
                    <button onclick="updateQuantity('${item._id}', 1)">+</button>
                </p>
                <button onclick="removeItem('${item._id}')">Remove</button>
            `;
            cartContainer.appendChild(cartItem);
        });

        totalPriceElement.textContent = `Ksh ${total}`;
    } catch (error) {
        console.error("Error loading cart:", error);
    }
}

// 🔹 Update quantity in MongoDB
async function updateQuantity(itemId, change) {
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${itemId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ change: change }),
        });

        if (!response.ok) {
            throw new Error("Failed to update quantity");
        }

        loadCart(); // Reload cart after updating
    } catch (error) {
        console.error("Error updating quantity:", error);
    }
}

// 🔹 Remove item from cart in MongoDB
async function removeItem(itemId) {
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${itemId}`, {
            method: "DELETE",
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error("Failed to remove item");
        }

        loadCart(); // Reload cart after removal
    } catch (error) {
        console.error("Error removing item:", error);
    }
}

// 🔹 Place order (Send cart to MongoDB and clear it)
async function placeOrder() {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error("Failed to place order");
        }

        alert("Order placed successfully!");
        loadCart(); // Reload cart (it should be empty now)
    } catch (error) {
        console.error("Error placing order:", error);
    }
}

// 🔹 Load cart on page load
document.addEventListener("DOMContentLoaded", loadCart);
