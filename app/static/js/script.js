"use strict";

(() => {

    // Wrap everything in an IIFE to avoid leaking variables into the global scope.

    // ==========================
    // HAMBURGER MENU
    // ==========================

    const hamburger = document.querySelector(".hamburger");
    const mobileMenu = document.querySelector(".mobile-menu");
    const menuOverlay = document.querySelector(".menu-overlay");

    // Variable to store the scroll position when the menu is opened.
    let scrollPosition = 0;

    function setMenuOpen(isOpen) {

        mobileMenu.classList.toggle("open", isOpen);
        menuOverlay.classList.toggle("active", isOpen);
        document.body.classList.toggle("menu-open", isOpen);

        // Prevent background scrolling when the menu is open.
        if (isOpen) {
            scrollPosition = window.scrollY;
            document.body.style.top = `-${scrollPosition}px`;
        } else {
            document.body.style.top = "";
            window.scrollTo(0, scrollPosition);
        }

        // Update ARIA attributes for accessibility.
        hamburger.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
        hamburger.setAttribute("aria-pressed", String(isOpen));
        mobileMenu.setAttribute("aria-hidden", String(!isOpen));
        hamburger.setAttribute("aria-expanded", String(isOpen));
        menuOverlay.setAttribute("aria-hidden", String(!isOpen));

    }

    if (hamburger && mobileMenu && menuOverlay) {

        // Toggle the menu open/closed when the hamburger icon is clicked.
        hamburger.addEventListener("click", () => {
            setMenuOpen(!mobileMenu.classList.contains("open"));
        });

        // Close the menu when clicking outside of it (menu overlay).
        menuOverlay.addEventListener("click", () => {
            setMenuOpen(false);
        });

        // Close the menu when pressing the Escape key.
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && mobileMenu.classList.contains("open")) {
                setMenuOpen(false);
            }
        });

        // Close the menu when clicking on any link inside it.
        mobileMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                setMenuOpen(false);
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

    // ==========================
    // PASSWORD VISIBILITY TOGGLE
    // ==========================

    function setupPasswordToggle(toggleId, inputId) {

        const eyeIcon = document.getElementById(toggleId);
        const passwordInput = document.getElementById(inputId);

        if (!eyeIcon || !passwordInput) {
            return;
        }

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

    setupPasswordToggle("togglePassword", "password");
    setupPasswordToggle("delete-toggle-password", "delete-password");

    // ==========================
    // DELETE ACCOUNT MODAL
    // ==========================

    // Get references to the modal elements
    const deleteBtn = document.getElementById("delete-account");
    const modal = document.getElementById("delete-modal");
    const cancelBtn = document.getElementById("cancel-delete");
    const deletePasswordInput = document.getElementById("delete-password");
    const confirmBtn = document.getElementById("confirm-delete");

    if (deleteBtn && modal && cancelBtn && deletePasswordInput && confirmBtn) {

        // Show the modal when the delete button is clicked
        deleteBtn.addEventListener("click", () => {
            modal.hidden = false;
        });

        // Hide the modal and reset the password input when the cancel button is clicked
        cancelBtn.addEventListener("click", () => {
            modal.hidden = true;
            deletePasswordInput.value = "";
            confirmBtn.disabled = true;
        });

        // Hide the modal when clicking outside of it (on the overlay)
        modal.addEventListener("click", (event) => {
            if (event.target === modal) {
                modal.hidden = true;
            }
        });

        // Enable or disable the confirm button based on whether the password input is empty
        deletePasswordInput.addEventListener("input", () => {
            confirmBtn.disabled = deletePasswordInput.value.length === 0;
        });

    }

})();