// DOM Ready Function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Event Search Functionality
    const eventSearch = document.getElementById('eventSearch');
    if (eventSearch) {
        eventSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const eventCards = document.querySelectorAll('.event-card');
            
            eventCards.forEach(card => {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const description = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    card.style.display = 'block';
                    card.classList.add('fade-in');
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Booking Confirmation
    const bookButtons = document.querySelectorAll('.book-event-btn');
    bookButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!this.classList.contains('disabled')) {
                const eventTitle = this.getAttribute('data-event-title');
                showToast(`🎟️ Booking confirmed for ${eventTitle}!`, 'success');
                
                // Disable button after click
                this.classList.add('disabled');
                this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
                
                // Simulate API call
                setTimeout(() => {
                    window.location.href = this.getAttribute('data-redirect-url');
                }, 1500);
            }
        });
    });

    // Seat Selection
    const seats = document.querySelectorAll('.seat-available');
    seats.forEach(seat => {
        seat.addEventListener('click', function() {
            if (this.classList.contains('seat-selected')) {
                this.classList.remove('seat-selected');
            } else {
                // Check max selection
                const maxSeats = parseInt(document.getElementById('ticketQuantity').value);
                const selectedSeats = document.querySelectorAll('.seat-selected').length;
                
                if (selectedSeats < maxSeats) {
                    this.classList.add('seat-selected');
                } else {
                    showToast(`You can only select ${maxSeats} seats.`, 'warning');
                }
            }
            updateSelectedSeats();
        });
    });

    // Update ticket quantity
    const ticketQuantity = document.getElementById('ticketQuantity');
    if (ticketQuantity) {
        ticketQuantity.addEventListener('change', function() {
            const maxSeats = parseInt(this.value);
            const selectedSeats = document.querySelectorAll('.seat-selected').length;
            
            if (selectedSeats > maxSeats) {
                showToast(`Reducing selection to ${maxSeats} seats.`, 'info');
                const seats = document.querySelectorAll('.seat-selected');
                for (let i = maxSeats; i < selectedSeats; i++) {
                    seats[i].classList.remove('seat-selected');
                }
            }
            updateSelectedSeats();
        });
    }

    // Countdown Timer for Events
    const countdownElements = document.querySelectorAll('.event-countdown');
    countdownElements.forEach(element => {
        const eventDate = new Date(element.getAttribute('data-event-date')).getTime();
        startCountdown(eventDate, element);
    });

    // Initialize image lazy loading
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img.lazy-load');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy-load');
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    }
});

// Helper Functions
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    const toastId = 'toast-' + Date.now();
    
    const toastHTML = `
        <div id="${toastId}" class="toast show fade" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Auto-remove toast after 5 seconds
    setTimeout(() => {
        const toastElement = document.getElementById(toastId);
        if (toastElement) {
            const toast = new bootstrap.Toast(toastElement);
            toast.hide();
            toastElement.addEventListener('hidden.bs.toast', () => {
                toastElement.remove();
            });
        }
    }, 5000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

function updateSelectedSeats() {
    const selectedSeats = Array.from(document.querySelectorAll('.seat-selected')).map(seat => seat.dataset.seatId);
    document.getElementById('selectedSeats').value = selectedSeats.join(',');
}

function startCountdown(eventDate, element) {
    function updateCountdown() {
        const now = new Date().getTime();
        const distance = eventDate - now;
        
        if (distance < 0) {
            element.innerHTML = '<div class="alert alert-warning">This event has started!</div>';
            return;
        }
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        element.innerHTML = `
            <div class="countdown">
                <div class="countdown-item">
                    <div class="countdown-value">${days}</div>
                    <div class="countdown-label">Days</div>
                </div>
                <div class="countdown-item">
                    <div class="countdown-value">${hours}</div>
                    <div class="countdown-label">Hours</div>
                </div>
                <div class="countdown-item">
                    <div class="countdown-value">${minutes}</div>
                    <div class="countdown-label">Mins</div>
                </div>
                <div class="countdown-item">
                    <div class="countdown-value">${seconds}</div>
                    <div class="countdown-label">Secs</div>
                </div>
            </div>
        `;
    }
    
    updateCountdown();
    const countdownInterval = setInterval(updateCountdown, 1000);
    
    // Cleanup when element is removed
    const observer = new MutationObserver(function(mutations) {
        if (!document.contains(element)) {
            clearInterval(countdownInterval);
            observer.disconnect();
        }
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
}

// Form Validation
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Special validation for password match
    const password = form.querySelector('#id_password1');
    const confirmPassword = form.querySelector('#id_password2');
    
    if (password && confirmPassword && password.value !== confirmPassword.value) {
        confirmPassword.classList.add('is-invalid');
        confirmPassword.nextElementSibling.textContent = 'Passwords do not match';
        isValid = false;
    }
    
    return isValid;
}