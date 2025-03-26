document.addEventListener("DOMContentLoaded", () => {
    const contactForm = document.getElementById("contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", sendMessage);
    }
});

async function sendMessage(event) {
    event.preventDefault();

    const name = document.getElementById("contact-name").value.trim();
    const email = document.getElementById("contact-email").value.trim();
    const message = document.getElementById("contact-message").value.trim();

    if (!name || !email || !message) {
        alert("Please fill out all fields.");
        return;
    }

    const contactData = { name, email, message };

    try {
        const response = await fetch("http://localhost:8000/api/contact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(contactData)
        });

        if (response.ok) {
            alert("Message sent successfully!");
            document.getElementById("contact-form").reset();
        } else {
            alert("Failed to send message. Try again.");
        }
    } catch (error) {
        console.error("Error sending message:", error);
        alert("Error occurred. Please try again.");
    }
}
