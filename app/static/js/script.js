"use strict";

(() => {

    // Wrap everything in an IIFE to avoid leaking variables into the global scope.

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

            // Keep ARIA state in sync for screen readers.
            hamburger.setAttribute("aria-expanded", String(isOpen));
            mobileMenu.setAttribute("aria-hidden", String(!isOpen));

        });


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

    const searchInput = document.getElementById("searchInput");
    const clearBtn = document.getElementById("clearBtn");

    if (searchInput && clearBtn) {

        searchInput.addEventListener("input", () => {

            if (searchInput.value.trim() !== "") {
                clearBtn.classList.add("visible");
            } else {
                clearBtn.classList.remove("visible");
            }

        });


        clearBtn.addEventListener("click", () => {

            searchInput.value = "";

            clearBtn.classList.remove("visible");

            searchInput.focus();

        });


        searchInput.addEventListener("keydown", (event) => {

            if (event.key === "Escape") {

                searchInput.value = "";

                clearBtn.classList.remove("visible");

            }

        });


        if (searchInput.value.trim() !== "") {
            clearBtn.classList.add("visible");
        }

    }


    // ==========================
    // DARK MODE TOGGLE
    // ==========================

    const themeToggles = document.querySelectorAll(".dark-mode-toggle");
    const icons = document.querySelectorAll(".dark-mode-toggle img");

    const savedTheme = localStorage.getItem("theme");


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
    // PASSWORD VISIBILITY TOGGLE
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


    // ==========================
    // RANDOM QUOTE
    // ==========================

    loadRandomQuote();


    async function loadRandomQuote() {

        const quoteElement = document.getElementById("quote");
        const authorElement = document.getElementById("author");


        if (!quoteElement || !authorElement) {
            return;
        }


        try {

            const response = await fetch("/static/data/quotes.json");

            if (!response.ok) {
                throw new Error("Could not load quotes");
            }


            const quotes = await response.json();

            // Pick one quote at random each time the page loads.
            const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];


            quoteElement.textContent = `"${randomQuote.quote}"`;
            authorElement.textContent = `— ${randomQuote.author}`;


        } catch (error) {

            console.error("Quote loading error:", error);

        }

    }

    // ==========================
    // HOMEPAGE CAROUSEL
    // ==========================

    const carousel = document.querySelector(".carousel");

    if (carousel) {

        const slides = carousel.querySelectorAll(".slide");
        const nextBtn = carousel.querySelector(".next");
        const prevBtn = carousel.querySelector(".prev");
        const dots = carousel.querySelectorAll(".dot");

        let currentIndex = 0;


        function updateCarousel() {

            // Reset active state, then activate the current slide and matching dot.

            slides.forEach(slide => {
                slide.classList.remove("active");
            });

            dots.forEach(dot => {
                dot.classList.remove("active");
            });

            slides[currentIndex].classList.add("active");

            if (dots[currentIndex]) {
                dots[currentIndex].classList.add("active");
            }

        }

        if (slides.length > 0) {
            updateCarousel();
        }


        if (nextBtn && prevBtn && slides.length > 0) {

            nextBtn.addEventListener("click", () => {


                currentIndex++;

                // Wrap to the first slide after the last one.
                if (currentIndex >= slides.length) {
                    currentIndex = 0;
                }

                updateCarousel();

            });


            prevBtn.addEventListener("click", () => {

                currentIndex--;

                // Wrap to the last slide when moving backward from the first.
                if (currentIndex < 0) {
                    currentIndex = slides.length - 1;
                }

                updateCarousel();

            });

        }

            dots.forEach((dot, index) => {

                dot.addEventListener("click", () => {

                    currentIndex = index;

                    updateCarousel();

                });
            });

            // AUTO-ROTATE CAROUSEL (every 3 seconds)

            let timer = setInterval(() => {

                currentIndex++;

                if (currentIndex >= slides.length) {
                    currentIndex = 0;
                }

                updateCarousel();

            }, 3000);


            // Pause auto-rotation when hovering over slides

            const sliderContainer = carousel.querySelector(".slider-carousel");


            sliderContainer.addEventListener("mouseenter", () => {

                clearInterval(timer);

            });


            sliderContainer.addEventListener("mouseleave", () => {

                timer = setInterval(() => {

                    currentIndex++;

                    if (currentIndex >= slides.length) {
                        currentIndex = 0;
                    }

                    updateCarousel();

                }, 3000);

            });

    }


})();