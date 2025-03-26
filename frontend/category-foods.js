document.addEventListener("DOMContentLoaded", () => {
    loadFoodItems();
    updateCart();
});

// Load food items from FastAPI (MongoDB)
async function loadFoodItems() {
    const foodList = document.getElementById("food-list");
    if (!foodList) return;

    foodList.innerHTML = "<p>Loading food items...</p>";

    try {
        const urlParams = new URLSearchParams(window.location.search);
        const categoryId = urlParams.get("category"); // Get category ID from URL

        const response = await fetch(`http://localhost:8000/api/foods?category=${categoryId}`); // Your FastAPI endpoint
        const foodItems = await response.json();

        if (!Array.isArray(foodItems) || foodItems.length === 0) {
            foodList.innerHTML = "<p>No food items available in this category.</p>";
            return;
        }

        foodList.innerHTML = foodItems.map(food => `
            <div class="food-menu-box">
                <form onsubmit="addToCart(event, '${food._id}', '${food.name}', ${food.price}, '${food.image}')">
                    <div class="food-menu-img">
                        <img src="${food.image}" class="img-responsive img-curve" alt="${food.name}">
                    </div>
                    <div class="food-menu-desc">
                        <h4>${food.name}</h4>
                        <p class="food-price">Ksh.${food.price}</p>
                        <p class="food-details">${food.description}</p>
                        <input type="number" name="quantity" min="1" value="1">
                        <input type="submit" class="btn-primary" value="Add to Cart">
                    </div>
                </form>
            </div>
        `).join("");

    } catch (error) {
        console.error("Error loading food items:", error);
        foodList.innerHTML = "<p>Failed to load food items. Please try again later.</p>";
    }
}

// Add food item to cart and store in localStorage
function addToCart(event, id, name, price, image) {
    event.preventDefault();

    const quantity = parseInt(event.target.querySelector("input[name='quantity']").value);
    if (quantity < 1) return;

    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    const existingItem = cart.find(item => item.id === id);

    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ id, name, price, image, quantity });
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    updateCart();
}

// Update cart display
function updateCart() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    
    const cartItems = document.getElementById("cart-items");
    const cartCount = document.getElementById("cart-count");
    const cartTotal = document.getElementById("cart-total");

    if (!cartItems || !cartTotal || !cartCount) return;

    cartItems.innerHTML = "";
    let total = 0;

    if (cart.length === 0) {
        cartItems.innerHTML = "<tr><td colspan='6' class='text-center'>Your cart is empty</td></tr>";
    } else {
        cart.forEach((item, index) => {
            let itemTotal = item.price * item.quantity;
            total += itemTotal;
            cartItems.innerHTML += `
                <tr>
                    <td><img src="${item.image}" alt="${item.name}" width="50"></td>
                    <td>${item.name}</td>
                    <td>Ksh.${item.price}</td>
                    <td>${item.quantity}</td>
                    <td>Ksh.${itemTotal}</td>
                    <td><a href="#" onclick="removeFromCart(${index})" class="btn-delete">&times;</a></td>
                </tr>
            `;
        });
    }

    cartTotal.textContent = `Ksh.${total}`;
    cartCount.textContent = cart.length;
}

// Remove item from cart
function removeFromCart(index) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.splice(index, 1);
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCart();
}
