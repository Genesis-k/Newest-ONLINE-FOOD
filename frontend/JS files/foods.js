const API_BASE_URL = "https://newest-online-food-production-up.railway.app/api/foods"; // Replace with actual backend URL

// Function to fetch and display food items
async function loadFoods() {
    try {
        const response = await fetch(API_BASE_URL);

        if (!response.ok) {
            throw new Error("Failed to fetch food items.");
        }

        const foods = await response.json();
        const foodContainer = document.getElementById("food-list");
        foodContainer.innerHTML = ""; // Clear previous content (Fixed syntax error)

        foods.forEach(food => {
            const foodItem = document.createElement("div");
            foodItem.classList.add("food-item");

            foodItem.innerHTML = `
                <img src="${food.image_url}" alt="${food.name}">
                <h3>${food.name}</h3>
                <p>${food.description || "No description available"}</p>
                <span>Ksh ${food.price}</span>
                <button onclick="addToCart('${food._id}', '${food.name}', ${food.price}, '${food.image_url}')">Add to Cart</button>
            `;

            foodContainer.appendChild(foodItem);
        });

    } catch (error) {
        console.error("Error fetching foods:", error);
        document.getElementById("food-list").innerHTML = "<p>Failed to load food items. Please try again.</p>";
    }
}

// Function to add food item to the cart (Stored in MongoDB)
async function addToCart(id, name, price, image_url) {
    const userId = localStorage.getItem("user_id"); // Ensure user is logged in
    if (!userId) {
        alert("Please log in to add items to your cart.");
        return;
    }

    try {
        const response = await fetch("https://newest-online-food-production-up.railway.app/api/cart", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
                user_id: userId,
                food_id: id,
                name,
                price,
                image_url,
                quantity: 1
            })
        });

        if (!response.ok) {
            throw new Error("Failed to add item to cart.");
        }

        alert(`${name} added to cart!`);
    } catch (error) {
        console.error("Error adding to cart:", error);
        alert("Failed to add item to cart. Try again.");
    }
}

// Load foods when the page loads
document.addEventListener("DOMContentLoaded", loadFoods);
