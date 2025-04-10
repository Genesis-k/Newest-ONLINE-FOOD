document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contact-form");
    const successMessage = document.getElementById("success-message");
    const API_BASE_URL = "https://newest-online-food-production-up.railway.app/api/contact"; // Replace with actual backend URL

    contactForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent form from reloading the page

        // Get form values
        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const subject = document.getElementById("subject").value.trim();
        const message = document.getElementById("message").value.trim();

        // Simple validation
        if (!name || !email || !phone || !subject || !message) {
            alert("All fields are required.");
            return;
        }

        // Prepare data for MongoDB
        const contactData = { name, email, phone, subject, message };

        try {
            const response = await fetch(API_BASE_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(contactData)
            });

            if (response.ok) {
                contactForm.reset();
                successMessage.textContent = "Your message has been sent successfully!";
                successMessage.style.color = "green";
            } else {
                successMessage.textContent = "Failed to send message. Try again later.";
                successMessage.style.color = "red";
            }
        } catch (error) {
            console.error("Error sending message:", error);
            successMessage.textContent = "An error occurred. Please try again.";
            successMessage.style.color = "red";
        }
    });
});
