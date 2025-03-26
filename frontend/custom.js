const backendURL ="newest-online-food-production.up.railway.app"
async function getFoodMenu() {
    try {
        const response = await fetch("https://newest-online-food-production.up.railway.app/foods"); // Replace with actual backend URL
        const data = await response.json();

        const menuContainer = document.getElementById("menu-items");
        menuContainer.innerHTML = "";

        data.forEach(food => {
            const foodItem = `
                <div class="food-menu-box">
                    <div class="food-menu-img">
                        <img src="${food.image_url}" class="img-responsive img-curve" alt="${food.name}">
                    </div>
                    <div class="food-menu-desc">
                        <h4>${food.name}</h4>
                        <p class="food-price">Ksh.${food.price}</p>
                        <p class="food-details">${food.description}</p>
                        <button class="btn-primary" onclick="addToCart('${food._id}', '${food.name}', ${food.price})">Add to Cart</button>
                    </div>
                </div>
            `;
            menuContainer.innerHTML += foodItem;
        });

    } catch (error) {
        console.error("Error fetching food menu:", error);
    }
}

getFoodMenu();

