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


})();