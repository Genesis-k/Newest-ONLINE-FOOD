async function loadOrders() {
    const response = await fetch(`${API_BASE_URL}/orders`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    const orders = await response.json();
    const orderList = document.getElementById("order-list");
    orderList.innerHTML = "";

    orders.forEach(order => {
        orderList.innerHTML += `
            <tr>
                <td>${order._id}</td>
                <td>${order.status}</td>
                <td>Ksh.${order.total_price}</td>
            </tr>
        `;
    });
}

document.addEventListener("DOMContentLoaded", loadOrders);
