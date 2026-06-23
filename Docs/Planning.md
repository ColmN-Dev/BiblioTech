# My Project Plan: BiblioTech Book Discovery App

## 1. My Vision for BiblioTech
I am building BiblioTech to serve as a personal digital bookshelf, wishlist organizer, and discovery companion. The name itself reflects this marriage of concepts: **"Biblio"** comes from the Greek word *biblion* (meaning book or scroll), which connects back to historical archives like the Great Library of Alexandria, while **"Tech"** represents the modern, dynamic computing systems we use to organize that information today. 

While working on my last project (GlobalGrub), everything was driven entirely by a local database. For BiblioTech, I want to expand my horizons by using the Google Books API as my main content engine. Since the API focuses on previews and shopping redirects rather than providing full texts, my app's core purpose is to help users discover new books, sample them, and manage their personal collections all in one place.

## 2. Core Features (What I want my users to do)
* **Interactive Live Search:** I want users to type any book title, author, or genre into a prominent search bar positioned directly underneath the navigation bar and instantly explore matching choices.
* **Real-Time Autocomplete Dropdown:** As soon as a user starts typing into the search bar, a clean dropdown panel will appear directly underneath the input field. It will display the closest matches with tiny cover thumbnails and book titles.
* **Daily Shifting Author Quote:** To make the site feel deeply literary, I want a dedicated space on the left side of the screen that introduces a random meaningful quote from a collection of 10 hardcoded quotes, accompanied simply by the name of the author. This quote shifts automatically once every 24 hours.
* **Automated Book Carousel:** Sitting directly to the right of the author quote, a visual banner displays 4 books fetched randomly from the Google Books API on each page load. This banner will automatically cycle from one book card to the next every 3 seconds to immediately catch the user's eye.
* **All-Genres Exploration Grid:** Lower down on the homepage, I want a complete, full-width visual grid of large, clickable block buttons representing all different genres (like Fiction, Sci-Fi, Mystery, Biography, and History) so undecided users can instantly browse books by their favorite category.
* **Dedicated Search Results Page with Pagination:** Submitting a search query or clicking a genre block will open a brand-new page featuring a balanced grid of 12 book cards at a time. To keep the view clean, the user can use "Next" and "Previous" page links at the bottom to browse through more results.
* **Detailed Book Profiles:** Clicking any book anywhere in the app will carry the user over to a spotlight page showcasing its full description, cover art, and two distinct destination links: one to read a free sample preview, and another pointing straight to where they can buy a copy.
* **My Library (Always Visible Navigation Shortcut):** The link for **My Library** will always be accessible right inside the main navigation bar. If a guest clicks it, the application will intercept the request and securely redirect them straight to the Login page to authenticate before viewing their personal shelves.
* **Reader Log (The Review & Star System):** On each individual book detail page, readers will find an entry form where they can leave a stamp on a book. They can select a rating from 1 to 5 stars using interactive star shapes and type a short note about their thoughts. Below the form, a live feed will show all reviews left for that book.
* **User Authentication Flow:** To protect personal spaces like **My Library** and the review system, I will implement a secure signup, login, and logout gateway using session-based tracking (or Flask-Login). Guests can freely browse and search across the app, but they must establish an authenticated session to save titles or post notes.

## 3. How I'm Handling the Navigation Flow
I want to give my users two smart, separate pathways to find books based on how fast they want to navigate:

1. **The Fast Track:** If a user types into the search bar right under the navbar and sees the exact book they want in the real-time floating autocomplete dropdown, they can click it to skip the search results grid entirely and jump straight to the full details profile page.
2. **The Scouting Track:** If a user types a general phrase and hits Enter (or clicks a genre block from the full grid lower down), they take the scenic route. The app opens the dedicated search results page, showing up to 12 book cards per page. Clicking any card from this grid then carries them to the final details profile page.

## 4. Visual Layout Concepts (My Whiteboard Blueprint)

### The Homepage Design (`index.html`)
* **Top Zone:** A clean horizontal navigation bar at the very top displaying links for Home, My Library, Login, and Sign Up. Directly underneath the navbar sits my central search input bar. Typing here dynamically drops down the floating real-time quick tray matching titles and thumbnail cover art.
* **Upper-Middle Zone:** A split presentation panel. The left side hosts the dynamic Daily Author Quote (showing the text quote and the author's name). The right side hosts the animated 4-book banner carousel sliding automatically every 3 seconds using randomized API results.
* **Bottom Zone:** A complete grid layout of large, inviting "All Genres" shortcut buttons to quickly pivot users straight into specific category results.

### The Search Results View (`search_results.html`)
* A structured grid showcasing up to 12 uniform book cards (arranged in a 3x4 grid). Each card contains the book cover image, title, author, and a "View Details" prompt.
* Balanced navigation options centered at the base of the screen: `[ <- Previous Page ]   Page X   [ Next Page -> ]`.

### The Spotlight View (`book_detail.html`)
* A clean split design. The left side anchors a large visual of the book cover art.
* The right side lists the main details (Title, Author, Summary) and a button to add the item directly to **My Library**, followed by two unmistakable action buttons: `[ Read Free Preview ]   [ Where to Buy ]`.
* **The Bottom Section:** A wide element containing the review block. It features an interactive row of 5 star shapes (`☆ ☆ ☆ ☆ ☆`) that change color when clicked, a text field box for typing a description, and a `[ Submit Review ]` button. Below this is a clean, vertical list card view displaying previous comments.

### The User Library View (`my_library.html`)
* A dedicated dashboard space displaying all the books the user has personally saved. This view acts as their private digital catalog, showing book tiles that link straight back to the book's full detail screen. This page requires a logged-in session; otherwise, it forces a routing shift to `login.html`.

### Authentication Views (`login.html` & `signup.html`)
* **Login Form (`login.html`):** A simplified form layout asking for existing credentials, along with a helpful contextual hyperlink pointing users to the signup template if they do not yet have an account.
* **Signup Form (`signup.html`):** A clean entry card requesting basic initialization metrics ( unique username and password parameters) to register a brand new active profile.

## 5. My Conceptual Model (How the Information Connects)
To map out how my application functions behind the scenes, I visualize a connected layout of structural components:

* **Component 1 (My Users):** Holds secure personal user profiles, usernames, and login credentials created whenever someone registers.
* **Component 2 (My Saved Books):** Keeps track of specific book metadata (title, cover image, API preview and purchase links). Crucially, our app acts like window shopping; it doesn't automatically save books to our local database tables during live API searches. A book is only remembered and permanently written to this table the exact second a user interacts with it (either by saving it or leaving a review).
* **Component 3 (The My Library Bridge):** An intersection table that securely links a specific **User ID** to a specific **Book ID**. This tracks exactly which items belong inside a user's custom collection screen.
* **Component 4 (The Reviews Space):** A separate interaction layer that links a **User ID and a Book ID** together, while carrying its own unique payload of information: the selected 1-to-5 star metric and the custom text thoughts typed out by that user. 
* *Note:* Although both Component 3 (My Library) and Component 4 (Reviews) associate a User ID with a Book ID, they will exist as two completely distinct data tables serving entirely separate operational roles within the schema layout.