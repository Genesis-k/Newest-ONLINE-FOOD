const API_BASE_URL = "https://newest-online-food-production-up.railway.app/api/category"; // Replace with actual backend URL
const CART_API_URL = "https://newest-online-food-production-up.railway.app/api/cart"; // Replace with cart API URL

// Function to fetch and display foods by category
async function loadFoodsByCategory() {
    const urlParams = new URLSearchParams(window.location.search);
    const categoryId = urlParams.get("category"); // Get category ID from URL

    try {
        let apiUrl = API_BASE_URL;
        if (categoryId) {
            apiUrl += `?category=${categoryId}`;
        }

        const response = await fetch(apiUrl);
        const foods = await response.json();

        const foodContainer = document.getElementById("food-list");
        foodContainer.innerHTML = ""; // Clear previous content

        if (foods.length === 0) {
            foodContainer.innerHTML = "<p>No foods available in this category.</p>";
            return;
        }

        foods.forEach(food => {
            const foodItem = document.createElement("div");
            foodItem.classList.add("food-item");

            foodItem.innerHTML = `
                <img src="${food.image}" alt="${food.name}">
                <h3>${food.name}</h3>
                <p>${food.description || "Delicious food item"}</p>
                <span>Ksh ${food.price}</span>
                <button onclick="addToCart('${food._id}', '${food.name}', ${food.price}, '${food.image}')">Add to Cart</button>
            `;
            foodContainer.appendChild(foodItem);
        });
    } catch (error) {
        console.error("Error fetching foods:", error);
    }
}

// Function to add item to cart (Now uses MongoDB instead of local storage)
async function addToCart(foodId, name, price, image) {
    const userId = sessionStorage.getItem("user_id"); // Ensure user is logged in
    if (!userId) {
        alert("Please log in to add items to your cart.");
        return;
    }

    const cartItem = {
        user_id: userId,
        food_id: foodId,
        name: name,
        price: price,
        image: image,
        quantity: 1
    };

    try {
        const response = await fetch(CART_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify(cartItem)
        });

        if (!response.ok) {
            throw new Error("Failed to add item to cart.");
        }

        alert(`${name} added to cart!`);
    } catch (error) {
        console.error("Error adding to cart:", error);
        alert("Could not add item to cart. Try again later.");
    }
}

// Load foods when the page loads
document.addEventListener("DOMContentLoaded", loadFoodsByCategory);
