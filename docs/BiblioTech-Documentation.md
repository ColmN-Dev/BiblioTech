# BiblioTech Documentation

**Last updated:** July 13, 2026

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
7. Planned Features vs Current State  
8. Current Limitations  
9. Key Design Decisions
10. Google Books API Integration  
11. API Reliability Improvements  
12. Review System
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

- run.py
- app/
  - __init__.py
  - config.py
  - models.py
  - routes.py
  - helpers.py
   - auth/
      - __init__.py
      - routes.py
  - templates/
  - static/

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

Routing is split by responsibility:

## Main Routes (`app/routes.py`)

| Route | Purpose |
|---|---|
| `/` | Homepage |
| `/search-results` | Search results |
| `/book/<book_id>` | Book details   |
| `/library` | User library (login required) |
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

The search route is connected to live Google Books API data, and book detail pages retrieve individual book information from the API.

---

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

---

# Planned Features vs Current State

## Planned Features

- Search autocomplete
- Genre filtering
- Account deletion

## Completed Features

- Flask application factory architecture with Blueprint routing, environment configuration, SQLAlchemy, Flask-Migrate, and deployment setup.
- Google Books API integration with search, book details, cover fallbacks, description sanitisation, marketplace links, timeout handling, and retry logic.
- Responsive frontend design including authentication pages, navigation improvements, mobile menu handling, homepage carousel, genre browsing, and search pagination.
- User authentication system using Flask-Bcrypt and Flask-Login with signup, login, logout, validation, and protected routes.
- Interactive homepage features including dynamic quotes, genre-based book carousel, automatic rotation, navigation controls, and indicators.
- Personal library CRUD functionality using the `User_Library` association table, including saving/removing books, duplicate prevention, saved book counts, account information, and timestamps.
- Review system allowing authenticated users to create, update, and delete reviews with 1-5 star ratings, review text, ownership checks, and database constraints.

---

# Current Limitations

1. Review aggregation features such as average user rating calculations are not currently implemented, as they were outside the current project scope.
2. Search autocomplete and advanced filtering features are still planned.
3. Google Books API thumbnails vary in aspect ratio and quality between books due to large dataset.

---

# Key Design Decisions

1. Adopted the Flask application factory pattern early to avoid future restructuring.
2. Used environment variables to separate sensitive configuration from application code.
3. Used Flask Blueprints to keep routes organised.
4. Initialised SQLAlchemy early to allow database development alongside application development.
5. Separated API logic into `helpers.py` to keep routes clean.
6. Used a `User_Library` association table instead of storing duplicate book data for each user.

---

# Google Books API Integration

API functionality is contained inside:

```text
app/helpers.py
```

## Functions

### `fetch_json(params, retries, url)`

Centralised API request handler.

Handles:

- HTTP errors
- Timeouts
- JSON parsing failures
- Retry attempts
- Missing API responses
- API key injection

The optional URL parameter allows the same request logic to be reused for both search requests and individual book detail requests.

Returns parsed JSON or `None`.

### `search_books(query, max_results, start_index, order_by)`

Searches books by:

- title
- author
- keyword

Used by the search route.

### `get_book_details(volume_id)`

Retrieves information about a single book.

Used by the book detail page.

### `get_random_books(count)`

Retrieves random books for homepage content, using genre-based subject searches.

---

# API Reliability Improvements

After integrating the Google Books API into the frontend, several reliability issues were discovered.

Improvements added:

- Centralised API requests
- Timeout handling
- Retry logic for temporary failures
- Differentiation between:
- API failure (`None`)
- Successful search with no results (`[]`)
- Fallback handling for missing book information

This prevents temporary API issues from incorrectly displaying "no results found".

---

## Review System

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

### User Interface

The review interface uses:
- CSS star rating selector.
- Responsive review cards.
- SVG icons for review actions.
- Styled review sections matching the BiblioTech theme.

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

# What Was Learned So Far

- Large Git refactors often represent organised restructuring rather than logic changes; Flask application factories, environment variables, and separated helper functions all improve scalability, security, and maintainability over single-file setups.
- Database relationships and migrations require careful planning; Flask-Migrate allows schema changes without manually recreating tables.
- External API data cannot be trusted at face value: responses need validation, sanitisation (e.g. stripping HTML markup), and defensive access patterns (`.get()` with defaults) since not every result includes every expected field.
- API failures and empty results should be handled separately, with retry logic (correctly scoped — a counter placed outside its loop can silently break the retry limit) improving reliability against temporary failures. Rotate API keys immediately if accidentally exposed.
- Getting genuinely varied results from an API often requires randomising more than the query itself (e.g. also randomising the result offset).
- Constructing third-party URLs requires the correct search path and query parameters, not just a domain and identifier.
- Frontend and responsive testing must happen with real API data, not placeholders, since layout and image-quality issues often only surface once live content is displayed.
- UI state (active indicators, scroll position, menu visibility) doesn't sync automatically — it must be explicitly managed, and consolidating that logic into a single function avoids triggers falling out of sync with each other.
- `overflow: hidden` alone isn't a reliable scroll lock on touch devices; `position: fixed` with manually preserved/restored scroll position is more robust.
- Mismatched or miscounted closing tags don't raise errors — they silently change element nesting, which can look like a CSS bug at first glance.
- Blueprint endpoint naming and import order matter in modular Flask refactors; using `auth.*` endpoint names and controlled blueprint registration avoids circular import issues.
- CRUD functionality requires careful separation between entity data and relationship data; association tables allow users to manage personal collections without duplicating shared external API information.

---

# Next Milestones

1. Implement account management features such as account deletion.
3. Add search improvements such as autocomplete and filtering.
4. Improve deployment and production testing.

---

# References

- Flask documentation:  
https://flask.palletsprojects.com/

- Flask SQLAlchemy:  
https://flask-sqlalchemy.palletsprojects.com/

- Flask Application Structure:  
https://www.colabcodes.com/post/flask-application-structure-organizing-python-web-apps-for-scalability

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

- Python Logging Documentation:  
https://docs.python.org/3/library/logging.html

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

- Flask-SQLAlchemy Relationships:
https://dev.to/freddiemazzilli/flask-sqlalchemy-relationships-exploring-relationship-associations-igo

- Flask-Login Documentation: 
https://flask-login.readthedocs.io/en/latest/