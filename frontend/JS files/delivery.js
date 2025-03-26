async function trackDelivery() {
    const orderId = document.getElementById("order-id").value;
    
    const response = await fetch(`${API_BASE_URL}/delivery?order_id=${orderId}`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    const delivery = await response.json();

    document.getElementById("delivery-status").textContent = delivery.status;
}
