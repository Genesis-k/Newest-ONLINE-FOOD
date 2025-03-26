document.addEventListener("DOMContentLoaded", loadCategories);

async function loadCategories() {
    const categoryList = document.getElementById("categories-list");
    if (!categoryList) return;

    categoryList.innerHTML = "<p>Loading categories...</p>";

    try {
        const response = await fetch("http://localhost:8000/api/categories"); // FastAPI endpoint
        const categories = await response.json();

        if (!Array.isArray(categories) || categories.length === 0) {
            categoryList.innerHTML = "<p>No categories found.</p>";
            return;
        }

        categoryList.innerHTML = categories.map(category => `
            <a href="foods.html?category=${category._id}">
                <div class="float-container">
                    <img src="${category.image}" class="img-responsive" alt="${category.name}">
                    <h3 class="float-text text-white">${category.name}</h3>
                </div>
            </a>
        `).join("");
    } catch (error) {
        console.error("Error loading categories:", error);
        categoryList.innerHTML = "<p>Failed to load categories.</p>";
    }
}
