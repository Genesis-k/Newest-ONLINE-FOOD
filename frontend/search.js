document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("search-form");
    if (searchForm) {
        searchForm.addEventListener("submit", searchFoods);
    }
});

async function searchFoods(event) {
    event.preventDefault();
    
    const searchInput = document.getElementById("search-input").value.trim();
    if (!searchInput) return;

    const foodList = document.getElementById("search-results");
    foodList.innerHTML = "<p>Searching...</p>";

    try {
        const response = await fetch(`http://localhost:8000/api/foods/search?query=${encodeURIComponent(searchInput)}`);
        const results = await response.json();

        if (!Array.isArray(results) || results.length === 0) {
            foodList.innerHTML = "<p>No matching foods found.</p>";
            return;
        }

        foodList.innerHTML = results.map(food => `
            <div class="food-menu-box">
                <a href="foods.html?food=${food._id}">
                    <div class="food-menu-img">
                        <img src="${food.image}" class="img-responsive img-curve" alt="${food.name}">
                    </div>
                    <div class="food-menu-desc">
                        <h4>${food.name}</h4>
                        <p class="food-price">Ksh.${food.price}</p>
                        <p class="food-details">${food.description}</p>
                    </div>
                </a>
            </div>
        `).join("");
    } catch (error) {
        console.error("Error searching foods:", error);
        foodList.innerHTML = "<p>Failed to search foods.</p>";
    }
}
