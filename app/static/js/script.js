"use strict";

(() => {

    // ==========================
    // HAMBURGER MENU
    // ==========================

    const hamburger = document.querySelector(".hamburger");
    const mobileMenu = document.querySelector(".mobile-menu");

    if (hamburger && mobileMenu) {

        hamburger.addEventListener("click", () => {

            mobileMenu.classList.toggle("open");
            document.body.classList.toggle("menu-open");

            const isOpen = mobileMenu.classList.contains("open");

            hamburger.setAttribute("aria-expanded", String(isOpen));
            mobileMenu.setAttribute("aria-hidden", String(!isOpen));

        });


        // Close mobile menu after selecting a link
        mobileMenu.querySelectorAll("a").forEach((link) => {

            link.addEventListener("click", () => {

                mobileMenu.classList.remove("open");
                document.body.classList.remove("menu-open");

                hamburger.setAttribute("aria-expanded", "false");
                mobileMenu.setAttribute("aria-hidden", "true");

            });

        });

    }

    // ==========================
    // SEARCH INPUT CLEAR BUTTON
    // ==========================

    document.addEventListener("DOMContentLoaded", () => {

    // Get the search input and clear button elements
    const searchInput = document.getElementById("searchInput");
    const clearBtn = document.getElementById("clearBtn");

    if (searchInput && clearBtn) {

        searchInput.addEventListener("input", () => {

            // Show or hide the clear button based on the input value
            if (searchInput.value.trim() !== "") {
                clearBtn.classList.add("visible");
            } else {
                clearBtn.classList.remove("visible");
            }

        });

    // Clear the search input when the clear button is clicked
    clearBtn.addEventListener("click", () => {

        searchInput.value = "";

        clearBtn.classList.remove("visible");

        searchInput.focus();

    });

    // Clear the search input when the Escape key is pressed
    searchInput.addEventListener("keydown", (e) => {

        if (e.key === "Escape") {

            searchInput.value = "";

            clearBtn.classList.remove("visible");

        }

    });

    // Show the clear button if the input has a value on page load
    if (searchInput.value.trim() !== "") {
        clearBtn.classList.add("visible");
    }

    }

    });



    // ==========================
    // DARK MODE TOGGLE
    // ==========================

    const themeToggles = document.querySelectorAll(".dark-mode-toggle");
    const icons = document.querySelectorAll(".dark-mode-toggle img");

    const savedTheme = localStorage.getItem("theme");


    // Load saved theme
    if (savedTheme === "dark") {

        document.documentElement.setAttribute("data-theme", "dark");

        icons.forEach(icon => {
            icon.src = "/static/images/sun.png";
        });

    } else {

        document.documentElement.setAttribute("data-theme", "light");

        icons.forEach(icon => {
            icon.src = "/static/images/moon.png";
        });

    }


    // Toggle theme 
    themeToggles.forEach(toggle => {

        toggle.addEventListener("click", () => {

            const currentTheme = document.documentElement.getAttribute("data-theme");

            if (currentTheme === "dark") {

                document.documentElement.setAttribute("data-theme", "light");

                localStorage.setItem("theme", "light");

                icons.forEach(icon => {
                    icon.src = "/static/images/moon.png";
                });

            } else {

                document.documentElement.setAttribute("data-theme", "dark");

                localStorage.setItem("theme", "dark");

                icons.forEach(icon => {
                    icon.src = "/static/images/sun.png";
                });

            }

        });

    });

    // ==========================
    // PASSWORD TYPE TOGGLE
    // ==========================

    const eyeIcon = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    if (eyeIcon && passwordInput) {
        eyeIcon.addEventListener("click", () => {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                eyeIcon.classList.add("closed");
                eyeIcon.classList.remove("open");
                eyeIcon.setAttribute("aria-label", "Hide password");
                eyeIcon.setAttribute("aria-pressed", "true");
            } else {
                passwordInput.type = "password";
                eyeIcon.classList.add("open");
                eyeIcon.classList.remove("closed");
                eyeIcon.setAttribute("aria-label", "Show password");
                eyeIcon.setAttribute("aria-pressed", "false");
            }
        });
    }


})();