(() => {
    "use strict";

    /* ============================
       MOBILE HAMBURGER MENU
       ============================ */

    const hamburger = document.querySelector(".hamburger");
    const mobileMenu = document.querySelector(".mobile-menu");

    if (hamburger && mobileMenu) {

        hamburger.addEventListener("click", () => {

            mobileMenu.classList.toggle("open");
            document.body.classList.toggle("menu-open");

            const isOpen = mobileMenu.classList.contains("open");

            hamburger.setAttribute(
                "aria-expanded",
                String(isOpen)
            );

            mobileMenu.setAttribute(
                "aria-hidden",
                String(!isOpen)
            );

        });
    }


    /* ============================
       DARK MODE TOGGLE
       ============================ */

    const toggle = document.getElementById("theme-toggle");
    const icon = document.getElementById("theme-icon");

    if (toggle && icon) {

        const savedTheme = localStorage.getItem("theme");

        if (savedTheme === "dark") {

            document.documentElement.setAttribute(
                "data-theme",
                "dark"
            );

            icon.src = "/static/images/sun.png";

        } else {

            document.documentElement.setAttribute(
                "data-theme",
                "light"
            );

            icon.src = "/static/images/moon.png";

        }


        toggle.addEventListener("click", () => {

            const currentTheme =
                document.documentElement.getAttribute("data-theme");


            if (currentTheme === "dark") {

                document.documentElement.setAttribute(
                    "data-theme",
                    "light"
                );

                icon.src = "/static/images/moon.png";

                localStorage.setItem(
                    "theme",
                    "light"
                );

            } else {

                document.documentElement.setAttribute(
                    "data-theme",
                    "dark"
                );

                icon.src = "/static/images/sun.png";

                localStorage.setItem(
                    "theme",
                    "dark"
                );

            }

        });

    }

})();