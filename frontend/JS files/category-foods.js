async function loadFoods() {
    const response = await fetch(`${API_BASE_URL}/foods`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    const foods = await response.json();
    displayFoods(foods);
}

function displayFoods(foods) {
    const foodList = document.getElementById("food-list");
    foodList.innerHTML = "";

    foods.forEach(food => {
        const foodHTML = `
            <div class="food-menu-box">
                <div class="food-menu-img">
                    <img src="${food.image}" class="img-responsive img-curve">
                </div>
                <div class="food-menu-desc">
                    <h4>${food.name}</h4>
                    <p class="food-price">Ksh.${food.price}</p>
                    <p class="food-details">${food.description}</p>
                    <button onclick="addToCart('${food._id}', '${food.name}', ${food.price})">Add to Cart</button>
                </div>
            </div>
        `;
        foodList.innerHTML += foodHTML;
    });
}

document.addEventListener("DOMContentLoaded", loadFoods);
