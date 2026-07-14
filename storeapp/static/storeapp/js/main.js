document.addEventListener("DOMContentLoaded", function () {
    // Mobile sidebar toggle for filters
    const filterToggle = document.getElementById("filterToggle");
    const sidebar = document.querySelector(".sidebar");
    if (filterToggle && sidebar) {
        filterToggle.addEventListener("click", function (e) {
            sidebar.classList.toggle("mobile-open");
            e.stopPropagation();
        });

        document.addEventListener("click", function(e) {
            if (sidebar.classList.contains("mobile-open") && !sidebar.contains(e.target) && e.target !== filterToggle) {
                sidebar.classList.remove("mobile-open");
            }
        });
    }

    // Clickable product rows & cards
    document.querySelectorAll(".product-row[data-href], .product-card[data-href]").forEach(function (element) {
        element.addEventListener("click", function (e) {
            // Prevent navigation if the user clicked on a link or button inside the card/row
            if (e.target.closest("a, button, input")) return;
            window.location.href = element.dataset.href;
        });
    });

    // Auto-dismiss alerts after 4 seconds with a smooth fade-out animation
    document.querySelectorAll(".alert").forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = "all 0.5s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            setTimeout(function () { 
                alert.remove(); 
            }, 500);
        }, 4000);
    });

    // Price input formatting hint: ensure 2 decimal places on blur
    const priceInput = document.querySelector('input[name="price"]');
    if (priceInput) {
        priceInput.addEventListener("blur", function () {
            const val = parseFloat(this.value);
            if (!isNaN(val)) {
                this.value = val.toFixed(2);
            }
        });
    }

    // Confirm deletion warning dialog
    const deleteForm = document.getElementById("deleteForm") || document.querySelector(".delete-card form");
    if (deleteForm) {
        deleteForm.addEventListener("submit", function (e) {
            // Only confirm if it's not already verified or if it's the simple button click
            const isConfirmed = confirm("Bu ilanı silmek istediğinize emin misiniz? Bu işlem geri alınamaz!");
            if (!isConfirmed) {
                e.preventDefault();
            }
        });
    }
});
