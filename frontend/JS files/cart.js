document.addEventListener("DOMContentLoaded", async () => {
    await loadCartItems();
});

// Fetch cart items from MongoDB
async function loadCartItems() {
    const response = await fetch("http://127.0.0.1:8000/api/cart");
    const cartItems = await response.json();

    const cartTable = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");

    cartTable.innerHTML = "";
    let totalPrice = 0;

    cartItems.forEach((item) => {
        totalPrice += item.price * item.quantity;
        cartTable.innerHTML += `
            <tr>
                <td><img src="${item.image}" width="50"></td>
                <td>${item.name}</td>
                <td>Ksh. ${item.price}</td>
                <td>${item.quantity}</td>
                <td>Ksh. ${item.price * item.quantity}</td>
                <td><button onclick="removeFromCart('${item._id}')">X</button></td>
            </tr>
        `;
    });

    cartTotal.textContent = `Ksh. ${totalPrice}`;
}

// Add item to cart
async function addToCart(foodId, name, price, image) {
    const response = await fetch("http://127.0.0.1:8000/api/cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ food_id: foodId, name, price, quantity: 1, image })
    });

    if (response.ok) {
        await loadCartItems();
    } else {
        console.error("Failed to add item to cart");
    }
}

// Remove item from cart
async function removeFromCart(itemId) {
    await fetch(`http://127.0.0.1:8000/api/cart/${itemId}`, { method: "DELETE" });
    await loadCartItems();
}

// Checkout
async function checkout(userId) {
    const response = await fetch(`http://127.0.0.1:8000/api/cart/checkout?user_id=${userId}`, {
        method: "POST"
    });

    if (response.ok) {
        alert("Order placed successfully!");
        await loadCartItems();
    } else {
        console.error("Checkout failed");
    }
}
