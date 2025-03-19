document.addEventListener('DOMContentLoaded', function() {
    const cartContent = document.getElementById('cart-content');
    const cartTable = cartContent.querySelector('.cart-table tbody');
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const cartBadge = document.querySelector('.badge');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const name = this.getAttribute('data-name');
            const price = this.getAttribute('data-price');
            const image = this.getAttribute('data-image');
            const qty = this.previousElementSibling.value;
            addItemToCart(name, price, image, qty);
        });
    });

    cartTable.addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-delete')) {
            event.preventDefault();
            const row = event.target.closest('tr');
            row.remove();
            updateCartTotal();
            updateCartBadge();
        }
    });

    function addItemToCart(name, price, image, qty) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><img src="${image}" alt="Food"></td>
            <td>${name}</td>
            <td>Ksh.${price}</td>
            <td><input type="number" value="${qty}" min="1" class="cart-qty"></td>
            <td>Ksh.${price * qty}</td>
            <td><a href="#" class="btn-delete">&times;</a></td>
        `;
        cartTable.appendChild(row);
        updateCartTotal();
        updateCartBadge();
    }

    function updateCartTotal() {
        let total = 0;
        cartTable.querySelectorAll('tr').forEach(row => {
            const price = parseFloat(row.cells[2].textContent.replace('Ksh.', ''));
            const qty = parseInt(row.cells[3].querySelector('input').value);
            total += price * qty;
            row.cells[4].textContent = `Ksh.${price * qty}`;
        });
        document.getElementById('cart-total').textContent = `Ksh.${total}`;
    }

    function updateCartBadge() {
        const itemCount = cartTable.querySelectorAll('tr').length;
        cartBadge.textContent = itemCount;
    }

    cartTable.addEventListener('change', function(event) {
        if (event.target.classList.contains('cart-qty')) {
            updateCartTotal();
        }
    });
});