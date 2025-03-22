const backendURL = "http://127.0.0.1:8000"; // Use backend URL when deployed

// Example: Fetch food menu from FastAPI
async function getFoodMenu() {
    try {
        const response = await fetch(`${backendURL}/foods`);
        const data = await response.json();
        console.log("Food Menu:", data);
    } catch (error) {
        console.error("Error fetching food menu:", error);
    }
}

getFoodMenu();
