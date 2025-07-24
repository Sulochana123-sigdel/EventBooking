// main.js

function confirmBooking(eventTitle) {
    alert(`🎉 You've booked: ${eventTitle}. Check your bookings.`);
}

// Live Search
document.addEventListener("DOMContentLoaded", () => {
    const search = document.getElementById("eventSearch");
    if (search) {
        search.addEventListener("input", () => {
            const value = search.value.toLowerCase();
            const cards = document.querySelectorAll(".event-card");
            cards.forEach(card => {
                const title = card.querySelector(".card-title").innerText.toLowerCase();
                card.style.display = title.includes(value) ? 'block' : 'none';
            });
        });
    }
});