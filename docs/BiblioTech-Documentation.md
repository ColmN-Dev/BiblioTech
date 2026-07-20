# BiblioTech Documentation

**Last updated:** July 21, 2026

---

# Table of Contents

1. Overview  
2. Project Development Summary  
   - Initial Structure  
   - Migration to Flask Application Factory Structure  
   - Runtime and Deployment  
3. Current Architecture  
   - Application Factory  
   - Configuration  
   - Entry Point  
   - Folder Structure (Updated With Auth Package)  
4. Current Routes  
   - Main Routes  
   - Auth Routes  
5. Frontend Status  
6. Database and Models  
7. Planned Features vs Completed Features 
8. Current Limitations  
9. Key Design Decisions
10. Google Books API Integration    
11. Review System
12. Account Management and Deletion System
13. Frontend Improvements  
14. Design Pattern Note: Facade  
15. Challenges Faced and Solutions  
16. What Was Learned So Far
17. Next Milestones  
18. References 

---

## Overview

BiblioTech is a Flask-based book discovery web application designed to allow users to search and explore books, create accounts, manage a personal library, and leave reviews on books.

The application uses the Google Books API as its external data source and has been restructured using a scalable Flask application factory architecture.

---

# Project Development Summary

## Initial Structure

The project originally used a simple flat Flask structure:

- app.py
- routes.py
- config.py
- models.py
- templates/
- static/

This structure was suitable for early development but became harder to maintain as additional features were introduced.

## Migration to Flask Application Factory Structure

The project was refactored into a package-based structure:

```text
run.py
app/
  __init__.py
  config.py
  models.py
  routes.py
  helpers.py
  auth/
    __init__.py
    routes.py
  templates/
  static/
```

This improved separation of responsibilities and provides a better foundation for future expansion.

## Runtime and Deployment

Deployment was updated to use:

`Procfile`

```text
web: gunicorn run:app
```

Local development runs through:

```text
python run.py
```

---

# Current Architecture

## Application Factory

`app/__init__.py` handles:

- Flask application creation
- Configuration loading
- SQLAlchemy initialisation
- Blueprint registration

## Application Data Flow

The application follows this general request flow:

```text
User Request
      |
      v
Flask Route
      |
      v
Helper Functions
      |
      +---- Cache Check
      |
      +---- Google Books API Request
      |
      +---- Data Processing
      |
      v
Jinja Template Rendering
```

## Configuration

`app/config.py` provides:

- `SECRET_KEY` from environment variables
- `SQLALCHEMY_DATABASE_URI`
- `SQLALCHEMY_TRACK_MODIFICATIONS = False`

Sensitive configuration is stored outside the codebase using environment variables.

## Entry Point

`run.py` imports `create_app()` and starts the application using environment-based configuration.

---

# Current Routes

Routing is split by responsibility using Flask Blueprints.

## Main Routes (`app/routes.py`)

| Route | Purpose |
|---|---|
| `/` | Homepage with featured books, genre categories, and carousel content |
| `/search-results` | Search results with pagination |
| `/auto-complete`  | Search Autocomplete and dropdown |
| `/book/<book_id>` | Book details, library actions, and reviews |
| `/book/<book_id>/review` | Create or update a book review (login required) |
| `/book/<book_id>/review/delete` | Delete a user's review (login required) |
| `/library` | User library (login required) |
| `/library/add/<book_id>` | Add a book to the user's library |
| `/library/remove/<book_id>` | Remove a book from the user's library |
| `/library/delete` | Account deletion with password confirmation |
| `/genre/<genre>` | Browse books by genre/category |
| `/about` | About page |

## Auth Routes (`app/auth/routes.py`)

| Route | Purpose |
|---|---|
| `/auth/login` | Login page / login handler |
| `/auth/signup` | Signup page / registration handler |
| `/auth/logout` | Logout handler |

Template links use blueprint-qualified endpoint names:

- `url_for('auth.login')`
- `url_for('auth.signup')`
- `url_for('auth.logout')`

The application uses Google Books API data for searching, book details, homepage content, and genre browsing. Database routes handle user-specific features including saved libraries, reviews, and account management.

# Frontend Status

Templates are stored in:

```text
app/templates/
```

and use Jinja template inheritance through `base.html`.

Current pages:

- Home
- Search results
- Book detail
- Your Library
- Login
- Signup
- About

Static assets:

```text
app/static/
```

Contains:

- CSS styling
- JavaScript files
- Images and branding assets
- Default book cover fallback image

---

# Database and Models

SQLAlchemy and Flask-Migrate are configured through the application factory.

Current models:

- User
- Book
- User_Library
- Review

## User

Stores account information:

- id
- username
- password_hash
- date_created

## Book

Stores Google Books API information:

- google_book_id (Primary Key)
- title
- authors
- cover_image
- buy_links
- date_created

## User_Library

Represents saved books.

Composite primary key:

- user_id
- google_book_id

Additional field:

- date_created

## Review

Stores user reviews:

- review_id
- user_id
- google_book_id
- rating
- review_text
- date_created

The `user_id` field allows NULL values so reviews can remain after an account is deleted. When a user account is removed, the review content is preserved and displayed as belonging to a deleted user rather than being permanently removed.

---

# Planned Features vs Completed Features

## Planned Features

- No current planned features

## Completed Features

- Flask application factory architecture with Blueprint routing, environment configuration, SQLAlchemy, Flask-Migrate, and deployment setup.
- Google Books API integration with search, book details, cover fallbacks, description sanitisation, marketplace links, timeout handling, and retry logic.
- Responsive frontend design including authentication pages, navigation improvements, mobile menu handling, homepage carousel, genre browsing, and search pagination.
- User authentication system using Flask-Bcrypt and Flask-Login with signup, login, logout, validation, and protected routes.
- Interactive homepage features including dynamic quotes, genre-based book carousel, automatic rotation, navigation controls, and indicators.
- Personal library CRUD functionality using the `User_Library` association table, including saving/removing books, duplicate prevention, saved book counts, account information, and timestamps.
- Review system allowing authenticated users to create, update, and delete reviews with 1-5 star ratings, review text, ownership checks, and database constraints.
- Account deletion system with password confirmation, database relationship handling, cascade deletion for saved books, and preservation of reviews from deleted accounts.
- Book detail genre matching recommendation list as a horizontal scroll with up to 12 results.
- Live search autocomplete with a debounced dropdown, keyboard-friendly clear button, and Escape-to-clear support.

---

# Current Limitations

1. No average rating calculation — outside scope.
2. Book cover quality/aspect ratio varies across the Google Books dataset.
3. API data can be unreliable. Action must be taken to mitigate API errors such as caching successful requests

---

# Key Design Decisions

1. Application factory pattern adopted early to avoid future restructuring.
2. Sensitive config kept in environment variables, not code.
3. Blueprints used to keep routing organised.
4. SQLAlchemy initialised early to develop the database alongside the app.
5. API logic separated into `helpers.py` to keep routes clean.
6. `User_Library` association table used instead of duplicating book data per user.

---

# Google Books API Integration

API functionality is contained inside:

```text
app/helpers.py
```

## Book Processing Functions

### `prepare_book(book)`

Processes raw Google Books API responses before they reach templates.

Handles:

- Adding external links.
- Adding Open Library fallback covers.
- Cleaning Google Books cover URLs.
- Selecting the final display cover image.

### `get_preferred_isbn(book)`

Extracts the best available ISBN from a Google Books API response.

Priority:

1. ISBN-13
2. ISBN-10

ISBN values are used for external links and Open Library cover fallback support.

### `has_isbn(book)`

Checks whether a book contains a usable ISBN.

Used when selecting books for the homepage carousel, ensuring only books with enough information are displayed.

### `has_cover(book)`

Checks whether Google Books provides a cover image.

Used to avoid displaying incomplete carousel entries.

### `add_custom_links(book)`

Creates external book links using ISBN data.

Generates links for:

- Amazon
- Goodreads
- WorldCat

### `add_openlibrary_cover(book)`

Creates an Open Library cover fallback URL using ISBN data when Google Books does not provide an image.

### `get_or_create_book(book_id)`

Checks whether a book already exists in the database.

If it does not:

1. Retrieves book details from Google Books API.
2. Creates a database record.
3. Stores reusable book information.

---

## API Functions

### `fetch_json(params, url)`

Centralised Google Books API request handler.

Handles:

- API key injection.
- Request caching.
- Timeouts.
- HTTP errors.
- Retry attempts.
- API failure logging.

Returns JSON data or `None`.

### `search_books(query, max_results, start_index)`

Searches Google Books and prepares returned books before sending them to templates.

Supports:

- Search queries.
- Pagination through `start_index`.
- Book preparation.

### `get_book_details(volume_id)`

Retrieves a single book using its Google Books volume ID.

Used by the book detail page.

### `get_books_by_subject(subject)`

Retrieves books based on a genre or category.

Used for genre browsing pages & More Like This section.

### `get_random_books(count)`

Generates homepage carousel content.

Uses:

- Random featured genres.
- API caching.
- Homepage caching.
- Cover and ISBN validation.

---

# Review System

### Overview

BiblioTech allows authenticated users to leave ratings and reviews on books. Users can create, update, and delete their own reviews, while all users (including guests) can view existing reviews.

### Database Design

Reviews are stored in the `reviews` table.

Fields:
- `review_id` - Primary key
- `user_id` - Foreign key linking the review to a user
- `google_book_id` - Foreign key linking the review to a book
- `rating` - Integer value between 1 and 5
- `review_text` - Optional written review
- `date_created` - Timestamp showing when the review was created

A unique constraint is applied to `user_id` and `google_book_id` to ensure each user can only submit one review per book.

---

### Review Functionality

Users can:

- Submit a rating and optional review text.
- Update their existing review.
- Delete their own review.
- View reviews submitted by other users.

Guests can view reviews but must log in to submit one.

### Security and Validation

Review actions require authentication using Flask-Login.

The system verifies ownership by checking the logged-in user's ID before allowing updates or deletion.

Ratings are validated server-side to ensure they are between 1 and 5.

Reviews remain available after account deletion through nullable user relationships. See User Account Deletion Relationships for the database behaviour.

### User Interface

The review interface uses:
- CSS star rating selector.
- Responsive review cards.
- SVG icons for review actions.
- Styled review sections matching the BiblioTech theme.

---

# Account Management and Deletion System

Account deletion was designed around preserving meaningful user-generated content while removing personal account data.

Deletion behaviour:

- User library entries are deleted using cascade behaviour because saved books only exist as part of a user's personal collection.
- Reviews are preserved after account deletion.
- Review ownership is removed by setting `user_id` to NULL.
- Deleted reviews display as "Deleted User" instead of attempting to access a missing account.

This avoids unnecessary data loss while preventing broken relationships.

---

# Frontend Improvements

Several frontend improvements were implemented after connecting API functionality to the user interface.

Improvements added:

- Improved authentication page styling using shared form layouts.
- Added password visibility toggle functionality using JavaScript.
- Added search input clearing through a clear button and Escape key support.
- Improved book detail layout for different screen sizes.
- Added fallback handling for long API-generated text.
- Added navigation buttons to improve movement between pages.
- Added dynamic homepage carousel using Google Books API data.
- Implemented responsive carousel behaviour across different screen sizes.
- Added fallback handling for books without available cover images.
- Added carousel navigation controls and slide indicators with active state styling to show the current slide.
- Added a curated 24-genre grid to the homepage, linking each genre to search results.
- Corrected marketplace buy link URLs on the book detail page.
- Added pagination controls to search results, including a sliding page-number window and a "Next" link gated on a full page of results.
- Added a full-screen overlay behind the mobile menu, allowing users to close it by clicking outside.
- Replaced the unreliable `overflow: hidden` scroll lock with a `position: fixed` approach that reliably prevents background scrolling on touch devices, restoring the user's scroll position on close.
- Added personal library interface with saved book grid, empty state handling, saved book count, and user account information.
- Added remove functionality from the library page with updated UI feedback.
- Added account deletion confirmation modal with password verification and safe cancellation behaviour.

The frontend uses responsive CSS techniques to maintain usability across desktop, tablet, and mobile devices.

---

# Design Pattern Note: Facade

A Facade pattern was considered for the API integration.

However, `helpers.py` currently contains simple stateless functions, meaning introducing a class-based facade would add unnecessary complexity.

A Facade may become useful in the future if BiblioTech expands to support multiple external APIs or shared API management logic.

---

# Challenges Faced and Solutions

## Challenge 1: Redesigning the ERD

### Challenge

The original ERD no longer matched the application's evolving requirements.

### Solution

DBdiagram.io was used to redesign relationships and understand primary keys, foreign keys, and relationship tables before implementing the database models.

---

## Challenge 2: Learning Flask-Migrate

### Challenge

Understanding database migrations and Flask CLI commands required additional research.

### Solution

Flask-Migrate was installed and configured through the application factory.

Commands were executed through Python:

```text
python -m flask db init
python -m flask db migrate -m "initial migration"
python -m flask db upgrade
```

This allowed migrations to run using the correct Python environment.

---

## Challenge 3: Designing Database Models

### Challenge

Designing relationships required understanding how tables connect and which fields should be primary or foreign keys.

### Solution

Each model was researched individually and refined until it matched the application requirements.

---

## Challenge 4: Refactoring Project Structure

### Challenge

The original Flask layout became difficult to manage as features increased.

### Solution

The project was reorganised into an application factory structure with separate configuration, models, routes, templates, and static files.

---

## Challenge 5: Google Books API Integration

### Challenge

API integration introduced several new challenges:

- External requests
- Error handling
- Environment variables
- Unexpected API responses

I also accidentally exposed my API key during testing by using a request URL that contained the key. The key was regenerated through Google Cloud Console, and `.env` was confirmed to be excluded using `.gitignore`.

After connecting search functionality to the frontend, intermittent failures were discovered where valid searches sometimes returned no results. Testing showed some requests received HTTP 503 responses from the API.

Additional frontend issues were discovered after integrating API data into templates. Some API descriptions contained HTML markup, which required cleaning before displaying to users.

Frontend testing also revealed layout issues on smaller screens, requiring improvements to wrapping behaviour, button positioning, and responsive styling.

### Solution

A central `fetch_json()` function was created to manage API requests and keep routes separated from external API logic.

The API layer was improved by adding:

- timeout handling
- HTTP error handling
- JSON validation
- retry attempts for temporary failures
- fallback handling for missing data

The application now differentiates between:

- API request failures (`None`)
- Successful searches with no matching results (`[]`)

This prevents temporary API issues from incorrectly displaying "no results found" to users.

HTML markup returned inside book descriptions was cleaned before rendering by using Python's `re` module to remove unwanted tags.

---

## Challenge 6: Building a Dynamic Homepage Carousel

### Challenge

Creating the homepage carousel introduced several frontend challenges when integrating live Google Books API data.

The initial implementation used randomly generated search queries, which produced inconsistent results because the API could return unrelated books or unsuitable content.

Additional issues were discovered during frontend testing:

- Carousel images used low-resolution API thumbnails, which caused quality issues when displayed at larger sizes.
- Responsive behaviour required adjustments across desktop, tablet, and mobile screen sizes.
- Carousel sizing required balancing image quality, layout space, and usability.
- Navigation controls and slide state management required JavaScript interaction to correctly switch between books.

### Solution

The random book generation system was improved by replacing random character searches with a predefined list of popular genres.

For example:

- Fiction
- Mystery
- Thriller
- Fantasy
- Science Fiction
- Biography
- History
- Science
- Adventure
- Romance
- Technology

The helper function was updated to randomly select genres and retrieve relevant books using Google Books API subject searches.

The carousel frontend was refined by:

- Adding responsive sizing adjustments using CSS media queries.
- Improving image display behaviour using object-fit styling.
- Adding fallback handling for missing book covers.
- Implementing JavaScript controls for previous and next navigation.
- Adding navigation indicators to show the active slide.
- Adding automatic slide rotation using `setInterval()`, resetting to the first slide at the end, with `mouseenter`/`mouseleave` pausing and resuming the timer.

Testing across different screen sizes highlighted the importance of designing components around real API data rather than placeholder content.

---

## Challenge 7: Book Detail Marketplace Links Not Resolving

### Challenge

Marketplace buy links (Amazon, Goodreads, WorldCat) on the book detail page did not resolve to valid search results.

### Solution

The URLs were being built by concatenating the domain directly with the ISBN (e.g. `https://amazon.com{isbn}`), with no search path or query parameter included. Corrected each link to use the proper search endpoint and query string for its platform (e.g. Amazon's `/s?k=`, Goodreads' and WorldCat's `/search?q=`), so the ISBN is passed as an actual search query rather than appended to the bare domain.

---

## Challenge 8: Carousel Navigation Dots Not Syncing with Active Slide

### Challenge

The carousel could move between slides correctly, but the navigation dots were only styled for hover — there was no logic tracking which dot corresponded to the currently visible slide.

### Solution

Updated the carousel JavaScript so that on every slide change it removes the `active` class from all dots, checks the current slide index, and re-applies `active` to the matching dot:

```javascript
dots.forEach(dot => dot.classList.remove("active"));
dots[currentIndex].classList.add("active");
```

This keeps the dot indicator in sync with the visible slide (Slide 1 → Dot 1, Slide 2 → Dot 2, etc.).

---

## Challenge 9: Carousel Images Not Displaying for Some Books

### Challenge

The carousel occasionally failed to display a cover image. Some books returned by the Google Books API did not include an `imageLinks` object or a `thumbnail` field, so JavaScript accessing `book.volumeInfo.imageLinks.thumbnail` directly would fail for those entries.

### Solution

Added fallback handling so the carousel checks whether a cover image actually exists before using it, defaulting to `no-cover.png` when it doesn't:

```python
cover = book_info.get("imageLinks", {}).get("thumbnail", "/static/images/no-cover.png")
```

This complements the genre-based query change from Challenge 6, since genre searches tend to return more relevant, better-catalogued books that are more likely to have a cover image in the first place.

---

## Challenge 10: Blurry Carousel and Book Cover Thumbnails

### Challenge

Once images displayed correctly, thumbnails appeared visibly blurry when scaled up, particularly in the carousel.

### Solution

Google Books' default thumbnail URLs return a low-resolution image (`zoom=1`). Resolved by using a regular expression to rewrite the `zoom` parameter to a higher value (`zoom=3`) for a sharper source image, combined with CSS (`object-fit: cover`) to keep images filling their containers cleanly. `object-fit: contain` was trialled for the carousel specifically to avoid cropping cover art, but reverted after testing showed the resulting whitespace looked worse across most books than the occasional bad crop under `cover`.

---

## Challenge 11: Intermittent "No Results" on Search and Carousel

### Challenge

Search results and the homepage carousel occasionally returned empty results on the first page load, with a subsequent reload succeeding for the exact same query. Testing showed this was linked to temporary Google Books API failures (e.g. HTTP 503 responses) that were not being retried.

An existing retry loop inside `get_random_books()` also contained a logic bug: the `attempts += 1` counter was indented outside the `while` loop rather than inside it, meaning the loop had no way to reliably terminate its own attempt count on repeated failure.

### Solution

Added matching retry logic to `search_books()`, using the same `attempts`-based `while` loop pattern already used in `get_random_books()`, so both functions retry up to three times before giving up and returning an empty list. Corrected the indentation bug so the attempt counter increments inside the loop as intended.

Standardising both functions on the same retry pattern keeps the API-handling logic consistent and easier to maintain going forward.

---

## Challenge 12: Homepage Carousel Always Showing the Same Books per Genre

### Challenge

The homepage carousel selected a random genre on each page load, but the same five books were returned every time for that genre, since Google Books always returns its most relevant results first for a given query with no offset applied.

### Solution

Added a randomised `startIndex` parameter to the request inside `get_random_books()`, so each request pulls from a random slice of the genre's results rather than always the top five:

```python
start_index = random.randint(0, 40)
```

The range was kept relatively low to avoid landing in thinly populated result ranges for less common genres, which had previously contributed to inconsistent or empty results.

A later restyling pass (switching carousel images to `object-fit: contain` and repositioning the navigation arrows beside the dots) briefly broke due to mismatched closing `</div>` tags placing `.carousel-nav` outside the `.carousel` container — corrected by fixing the nesting.

---

## Challenge 13: Search Results Pagination

### Challenge

Search results only ever displayed a single page of results (fixed at `maxResults`), with no way for users to browse further into a larger result set.

### Solution

Added a `start_index` parameter to `search_books()`, calculated in the route from a `page` query parameter:

```python
per_page = 20
start_index = (page - 1) * per_page
```

The template renders a sliding window of page-number links centred on the current page, rather than a fixed range, so the pagination bar stays consistent in width as the user moves through results:

```jinja
{% set window = 2 %}
{% set start_page = [1, page - window]|max %}
{% set end_page = start_page + 4 %}
```

Since Google Books' `totalItems` figure is an estimate and unreliable for exact page-count calculations, the "Next" link is only shown when the current page returned a full set of results (`results|length == per_page`), which is a more reliable signal that further pages likely exist.

---

## Challenge 14: Mobile Menu Not Closing on Outside Click and Background Still Scrollable

### Challenge

The mobile navigation menu could only be closed by clicking a link inside it; clicking anywhere else on the page did nothing. Additionally, `overflow: hidden` on the `body` element was not reliably preventing the background page from scrolling while the menu was open on touch devices.

### Solution

Added a full-screen overlay element that appears behind the menu (but above the rest of the page) whenever the menu is open. Clicking the overlay closes the menu using the same handler as the nav links, giving users a natural "click away to close" interaction.

For the scroll issue, switched `body.menu-open` from `overflow: hidden` to `position: fixed`, which reliably prevents scrolling on touch devices by removing the body from the normal scrollable document flow entirely. The page's scroll position is recorded in JavaScript before the menu opens and restored with `window.scrollTo()` after it closes, so the user returns to where they were rather than being left at the top of the page.

All menu-state changes (open/close, overlay visibility, body lock, ARIA attributes) were consolidated into a single `setMenuOpen(isOpen)` function, called by the hamburger button, the overlay, and each nav link, to avoid duplicating the same logic in three places.

---

## Challenge 15: Splitting Auth Routes into `app/auth/routes.py`

### Challenge

When authentication routes were moved from `app/routes.py` into `app/auth/routes.py`, three issues appeared during integration:

- Existing links still pointed to old endpoint names and needed to be updated to `auth.*` endpoints.
- A circular import risk appeared between `app/__init__.py` and `app/auth/routes.py` during blueprint registration.
- Model relationship references required debugging during auth/database wiring.

### Solution

- Registered the auth blueprint through the application factory with import order set to avoid circular imports.
- Updated endpoint usage in templates and redirects to `auth.login`, `auth.signup`, and `auth.logout`.
- Added and validated required `db.relationship(...)` references and fixed broken references uncovered during debugging.

---

## Challenge 16: Implementing User Library CRUD Functionality

### Challenge

After authentication was completed, the next step was allowing users to create personal book collections.

The main challenge was designing the relationship between users and books. Storing full API data for every saved book would duplicate external Google Books information unnecessarily, while multiple users needed to be able to save the same book.

### Solution

A `User_Library` association table was created to represent the many-to-many relationship between users and books.

The table uses a composite primary key:

- `user_id`
- `google_book_id`

This prevents duplicate saves while allowing multiple users to save the same book.

When a user saves a book:

1. The book details are stored in the `Book` table.
2. A relationship entry is created in `User_Library`.
3. The library page retrieves saved books through this relationship.

Removing a book only removes the `User_Library` relationship, preserving shared book data.

Additional features added:
- Saved book count display.
- Username and account creation date display.
- Book save timestamps.
- Remove functionality from library and book detail pages.

This reinforced the importance of separating entity data from relationship data.

---

## Challenge 17: Implementing Review Functionality

### Challenge

Adding reviews required designing how user-generated content would relate to existing users and books. The system needed to allow multiple users to review the same book while preventing individual users from submitting duplicate reviews for the same book.

Additional considerations included ensuring users could only modify or delete their own reviews.

### Solution

A `Review` model was created with relationships to both the `User` and `Book` models.

A unique constraint was added to the combination of `user_id` and `google_book_id` to ensure each user can only have one review per book.

Flask-Login authentication was used to protect review actions, and ownership checks were implemented before allowing users to update or delete reviews.

The review system now supports:
- creating reviews
- updating existing reviews
- deleting reviews
- displaying reviews to all users, including guests

---

## Challenge 18: Implementing Account Deletion

### Challenge

Deleting user accounts required deciding how related data should behave. Removing everything would unnecessarily delete useful user-generated content such as reviews, while keeping personal data could leave invalid relationships.

Additional frontend challenges included implementing a safe confirmation flow and ensuring the modal behaved correctly.

### Solution

Account deletion was implemented with password confirmation before permanently removing the account.

Database decisions:

- Saved books are deleted automatically using cascade deletion because they represent personal user collections.
- Reviews remain after account deletion.
- Review `user_id` was changed to allow NULL values.
- Deleted reviews display "Deleted User".

Frontend improvements included:

- Confirmation modal before deletion.
- Password input requirement.
- Disabled delete button until a password is entered.
- Click-outside modal closing.
- Password visibility toggle support.

Database migrations were required after changing model constraints to keep the database schema synchronized with SQLAlchemy models.

---

### Challenge 19: Google Books API Reliability and Request Caching

### Challenge

Search, carousel, and genre pages occasionally failed during development, initially suggesting frontend issues because failures appeared inconsistent between different parts of the application.

Logging was added to the API request layer to capture the actual responses from Google Books. This revealed temporary API failures including HTTP 503 responses and rate limiting responses rather than frontend problems.

Further investigation showed that repeated development testing combined with retry logic could generate unnecessary API requests and contribute to reaching the daily API quota.

### Solution

The API request system was improved by adding an in-memory TTL cache inside `fetch_json()`.

The cache stores successful API responses and reuses them for a defined period, reducing repeated requests for identical queries.

Current improvements include:

- API response caching using timestamps.
- Separate homepage carousel caching.
- Reduced retry attempts for failed requests.
- Immediate stopping on HTTP 429 quota responses.
- Improved logging of API failures.

Current cache settings:

- API responses: 6 hours.
- Homepage carousel results: 6 hours.

This reduces unnecessary external requests while improving reliability during normal application usage.

---

### Challenge 20: Challenge 20: Implementing Search Autocomplete
 
### Challenge
 
Search autocomplete needed to suggest book titles as the user typed, without flooding the backend with a request on every keystroke, and without duplicating the clear-button logic already used elsewhere in the search input.
 
An initial "ghost text" approach was attempted first — showing an inline, greyed-out completion directly inside the search box, similar to some search engines' (e.g Google) inline suggestion style. This was scrapped after testing, since positioning the overlay text correctly against the real input value added significant complexity for limited UX benefit over a standard dropdown.
 
### Solution
 
Replaced the ghost-text approach with a conventional dropdown suggestion list, built around three pieces:
 
1. **Debounced fetch** — a `setTimeout`/`clearTimeout` pattern delays the request until the user pauses typing for roughly a quarter of a second, rather than firing a request on every keystroke.
2. **A dedicated `/auto-complete` route**, queried once the debounce timer completes, returning a JSON list of matching titles.
3. **A shared `clearSuggestions()`/`clearAutocomplete()` helper**, reused by the dropdown rendering logic, the clear button, and the Escape key handler, so the "wipe the suggestions list" behaviour lives in one place rather than being repeated across handlers.
The dropdown's visibility is controlled with a single `.open` CSS class toggled via `classList`, in line with the project's existing preference for class-based state changes over direct inline style manipulation in JavaScript.
 
Clicking a suggestion fills the search input with the selected title and clears the dropdown, matching the interaction pattern of the existing clear button.
 
---

# What Was Learned So Far

- Refactors (application factories, env variables, separated helpers) are usually organisational improvements, not logic changes — they pay off in scalability and maintainability.
- Flask-Migrate handles schema changes safely without recreating the database, but migrations must be planned around relationships.
- External API data needs defensive handling: `.get()` defaults, validation, and sanitisation, since responses are often incomplete.
- API failures (`None`) and empty results (`[]`) must be handled separately; retry logic covers temporary failures, and nested retry loops can multiply request volume fast enough to exhaust quota. Exposed keys should be rotated immediately.
- Caching can significantly improve reliability when working with external APIs. Storing successful responses temporarily reduces unnecessary requests, improves loading times, and helps avoid hitting third-party rate limits.
- Reliable integration is more than the query itself — offsets, URL construction, and third-party parameters all need correct handling.
- Frontend issues (layout, image quality, responsiveness) often only surface with real API data, not placeholders.
- UI state (menus, carousels, modals) needs centralised logic to stay consistent.
- Some responsive issues need more than CSS — e.g. `position: fixed` with scroll restoration beats `overflow: hidden` for mobile scroll locking.
- Small HTML nesting errors can silently break CSS behaviour.
- Blueprints need consistent endpoint naming and careful import order to avoid circular imports.
- CRUD design should separate entity data from relationship data via association tables, avoiding duplication.
- Account deletion is a data lifecycle decision: cascade personal relationship data, but preserve user-generated content with identifiers removed where meaningful.

---

# Next Milestones

1. Improve deployment and production testing.

---

# References

- Flask documentation:  
https://flask.palletsprojects.com/

- Flask SQLAlchemy:  
https://flask-sqlalchemy.palletsprojects.com/

- Flask Configuration Handling:  
https://flask.palletsprojects.com/en/latest/config/

- Flask-Migrate documentation:  
https://flask-migrate.readthedocs.io/

- Gunicorn documentation:  
https://docs.gunicorn.org/

- Google Books API:  
https://developers.google.com/books/docs/v1/using

- DBdiagram.io:  
https://dbdiagram.io/

- python-dotenv:  
https://pypi.org/project/python-dotenv/

- Requests documentation:  
https://requests.readthedocs.io/

- Flask Error Handling:  
https://flask.palletsprojects.com/en/latest/errorhandling/

- HTTP Status Codes Reference:  
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

- REST API Design Best Practices:  
https://restfulapi.net/

- Flask Blueprints:  
https://flask.palletsprojects.com/en/latest/blueprints/

- Flask Application Factories:  
https://flask.palletsprojects.com/en/latest/patterns/appfactories/

- Alembic Migration Tool:  
https://alembic.sqlalchemy.org/

- Pagination with Python:  
https://www.geeksforgeeks.org/python/how-to-do-pagination-in-python/

- Flask-Login Documentation: 
https://flask-login.readthedocs.io/en/latest/

- Flask Bcrypt Documentation:
https://flask-bcrypt.readthedocs.io/en/1.0.1/

- Flask Sessions Documentation:  
https://flask.palletsprojects.com/en/latest/api/#sessions

- Flask-SQLAlchemy Cascades:
https://docs.sqlalchemy.org/en/21/orm/cascades.html

- Custom Python Cache Implementation:
https://medium.com/@saleem.latif.ee/implementing-a-custom-cache-in-python-68c39ece8a8

- Python functools.lru_cache documentation:  
https://docs.python.org/3/library/functools.html#functools.lru_cache

- Python Logging Documentation:
https://docs.python.org/3/library/logging.html