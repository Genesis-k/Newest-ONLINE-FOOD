const API_BASE_URL = "https://newest-online-food-production-up.railway.app/api/foods/search"; // Replace with actual backend URL

// Function to handle food search
async function searchFoods() {
    const searchInput = document.getElementById("search-input").value.trim(); // Ensure correct property usage
    const foodContainer = document.getElementById("search-results");

    // Validate search input
    if (!searchInput) {
        foodContainer.innerHTML = "<p>Please enter a search term.</p>";
        return;
    }

    try {
        // Fetch search results from the backend
        const response = await fetch(`${API_BASE_URL}?query=${encodeURIComponent(searchInput)}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to fetch search results.");
        }

        const foods = await response.json();
        foodContainer.innerHTML = ""; // Clear previous results

        // Handle no results
        if (foods.length === 0) {
            foodContainer.innerHTML = "<p>No matching foods found.</p>";
            return;
        }

        // Display search results
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
        console.error("Error fetching search results:", error);
        foodContainer.innerHTML = `<p>${error.message || "Error fetching search results. Please try again."}</p>`;
    }
}

// Function to add item to cart (now stored in MongoDB)
async function addToCart(id, name, price, image) {
    const userId = localStorage.getItem("user_id"); // Ensure user is logged in
    if (!userId) {
        alert("Please log in to add items to your cart.");
        return;
    }

    try {
        // Send POST request to add item to cart
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
                image,
                quantity: 1
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to add item to cart.");
        }

        alert(`${name} added to cart!`);
    } catch (error) {
        console.error("Error adding to cart:", error);
        alert(error.message || "Failed to add item to cart. Try again.");
    }
}

// Add event listener for search button
document.getElementById("search-button").addEventListener("click", searchFoods);

// Enable search on pressing Enter
document.getElementById("search-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        searchFoods();
    }
});
