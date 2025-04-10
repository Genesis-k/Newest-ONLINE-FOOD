const API_BASE_URL = "https://newest-online-food-production-up.railway.app/api/categories"

//function to fetch and display categories
async function loadCategories() {
    try {
        const response = await fetch(API_BASE_URL);
        const categories = await response.json();

        const categoryContainer = document.getElementById("category-list");
        categoryContainer.innerHTML = ""// clear previous content

        categories.forEach(category => {
            const categoryItem = document.createElement("div");
            categoryItem.classList.add("category-item");

            categoryItem.innerHTML = `
            <img src ="${category.image}" alt="${category.name}">
            <h3>${category.name}</h3>
            <button onclick="filterFoods('${category._id}')">View</button>
            `;
            categoryContainer.appendChild(categoryItem);
        });
    } catch (error) {
        console.error("Error fetching categories:", error);
    }
}
// function to filter foods by category
function filterFoods(categoryId) {
    window.location.href = `foods.html?category=${categoryId}`;
}
//Load categories when the pages loads
document.addEventListener("DOMContentLoaded", loadCategories);