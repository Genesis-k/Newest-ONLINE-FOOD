async function searchFoods() {
    const query = document.getElementById("search-input").value;

    const response = await fetch(`${API_BASE_URL}/foods/search?query=${query}`);
    const foods = await response.json();

    const foodList = document.getElementById("food-list");
    foodList.innerHTML = "";

    foods.forEach(food => {
        foodList.innerHTML += `
            <div class="food-menu-box">
                <h4>${food.name}</h4>
                <p class="food-price">Ksh.${food.price}</p>
            </div>
        `;
    });
}
