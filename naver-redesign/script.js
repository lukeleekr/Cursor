document.addEventListener('DOMContentLoaded', () => {
    // Clock functionality
    const clockElement = document.getElementById('clock');

    function updateClock() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        clockElement.textContent = `${hours}:${minutes}`;
    }

    if (clockElement) {
        updateClock();
        setInterval(updateClock, 1000);
    }

    // Search Input Animation
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');

    // Add a subtle shake effect if empty on submit
    searchForm.addEventListener('submit', (e) => {
        if (!searchInput.value.trim()) {
            e.preventDefault();
            searchForm.style.animation = 'shake 0.4s cubic-bezier(.36,.07,.19,.97) both';

            setTimeout(() => {
                searchForm.style.animation = '';
            }, 400);
        }
    });

    // Add CSS for shake animation dynamically
    const styleSheet = document.createElement("style");
    styleSheet.innerText = `
        @keyframes shake {
            10%, 90% { transform: translate3d(-1px, 0, 0); }
            20%, 80% { transform: translate3d(2px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
            40%, 60% { transform: translate3d(4px, 0, 0); }
        }
    `;
    document.head.appendChild(styleSheet);
});
