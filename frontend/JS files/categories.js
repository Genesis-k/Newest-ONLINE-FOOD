const token = localStorage.getItem("token");

async function loadCategories() {
    const response = await fetch(`${API_BASE_URL}/categories`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    const categories = await response.json();
    const categoryList = document.getElementById("category-list");
    categoryList.innerHTML = "";

    categories.forEach(category => {
        const categoryHTML = `
            <div class="category-box">
                <h4>${category.name}</h4>
                <button onclick="loadFoodsByCategory('${category.name}')">View Foods</button>
            </div>
        `;
        categoryList.innerHTML += categoryHTML;
    });
}

async function loadFoodsByCategory(categoryName) {
    const response = await fetch(`${API_BASE_URL}/foods?category=${categoryName}`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    const foods = await response.json();
    displayFoods(foods);
}

document.addEventListener("DOMContentLoaded", loadCategories);
