/* ==========================================================================
   BUSINESS OS - INTERACTIVE FRONTEND JS CONTROLLER (LIGHTWEIGHT ARCHITECTURE)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile Menu Toggle Controller
    const mobileMenuBtn = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener("click", () => {
            mobileMenu.classList.toggle("hidden");
            
            // Toggle icon classes between bars and times if using icons
            const icon = mobileMenuBtn.querySelector("i");
            if (icon) {
                if (mobileMenu.classList.contains("hidden")) {
                    icon.className = "fa-solid fa-bars text-xl";
                } else {
                    icon.className = "fa-solid fa-xmark text-xl";
                }
            }
        });
        
        // Auto-close menu when a link inside is clicked
        const mobileLinks = mobileMenu.querySelectorAll("a");
        mobileLinks.forEach(link => {
            link.addEventListener("click", () => {
                mobileMenu.classList.add("hidden");
                const icon = mobileMenuBtn.querySelector("i");
                if (icon) icon.className = "fa-solid fa-bars text-xl";
            });
        });
    }

    // 2. Dynamic Navbar Scroll Hardening Blur Effect
    const navbar = document.querySelector("nav");
    if (navbar) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 20) {
                navbar.style.paddingTop = "12px";
                navbar.style.paddingBottom = "12px";
                navbar.style.background = "rgba(11, 15, 25, 0.85)";
            } else {
                navbar.style.paddingTop = "16px";
                navbar.style.paddingBottom = "16px";
                navbar.style.background = "rgba(17, 24, 39, 0.55)";
            }
        });
    }
});
