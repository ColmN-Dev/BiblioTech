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

    // Initialize the current slide index and timer variable.
    let currentIndex = 0;
    let timer = null;


    // Updates the visible slide and active navigation dot.
    function updateCarousel() {

        // Prevent errors if no slides were returned from the API.
        if (slides.length === 0) {
            return;
        }


        // Safety checks to keep index within valid range.
        if (currentIndex >= slides.length) {
            currentIndex = 0;
        }

        if (currentIndex < 0) {
            currentIndex = slides.length - 1;
        }


        // Remove active state from all slides.
        slides.forEach(slide => {
            slide.classList.remove("active");
        });


        // Remove active state from all dots.
        dots.forEach(dot => {
            dot.classList.remove("active");
        });


        // Activate current slide.
        slides[currentIndex].classList.add("active");


        // Activate matching navigation dot.
        if (dots[currentIndex]) {
            dots[currentIndex].classList.add("active");
        }

    }

    // Start carousel timer.
    function startAutoRotate() {

        // Do not start timer if there is only one or no slides.
        if (slides.length <= 1) {
            return;
        }


        // Prevent multiple timers running at once.
        clearInterval(timer);


        timer = setInterval(() => {

            currentIndex++;


            // Return to first slide after reaching the end.
            if (currentIndex >= slides.length) {
                currentIndex = 0;
            }


            updateCarousel();


        }, 3000);

    }

    // Stop carousel timer.
    function stopAutoRotate() {

        clearInterval(timer);

    }

    // Initialise carousel on page load.
    updateCarousel();

    startAutoRotate();

    // Next button functionality.
    if (nextBtn) {

        nextBtn.addEventListener("click", () => {

            currentIndex++;


            if (currentIndex >= slides.length) {
                currentIndex = 0;
            }


            updateCarousel();

        });

    }

    // Previous button functionality.
    if (prevBtn) {

        prevBtn.addEventListener("click", () => {

            currentIndex--;


            if (currentIndex < 0) {
                currentIndex = slides.length - 1;
            }


            updateCarousel();

        });

    }

    // Navigation dot functionality.
    dots.forEach((dot, index) => {

        dot.addEventListener("click", () => {


            // Only allow indexes that actually have slides.
            if (slides[index]) {

                currentIndex = index;

                updateCarousel();

            }

        });

    });

    // Pause carousel while hovering over the slider.
    const sliderContainer = carousel.querySelector(".slider-carousel");


    if (sliderContainer) {

        sliderContainer.addEventListener("mouseenter", () => {

            stopAutoRotate();

        });



        sliderContainer.addEventListener("mouseleave", () => {

            startAutoRotate();

        });

    }

}


})();