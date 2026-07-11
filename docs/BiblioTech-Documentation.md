# BiblioTech Documentation

**Last updated:** July 11, 2026

---

## Overview

BiblioTech is a Flask-based book discovery web application designed to allow users to search and explore books, with future support for user accounts, reviews, and personal library features.

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

`app/routes.py` currently provides:

| Route | Purpose |
|---|---|
| `/` | Homepage |
| `/search` | Search results |
| `/book/<book_id>` | Book details |
| `/library` | User library placeholder |
| `/auth/login` | Login page |
| `/auth/signup` | Signup page |
| `/auth/logout` | Clears session |

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
- Authentication
- Personal library system
- Reviews and ratings

## Completed Features

- Flask application factory architecture
- Blueprint routing
- SQLAlchemy integration
- Flask-Migrate setup
- Database schema creation
- Model implementation
- Deployment configuration
- Environment-based configuration
- Google Books API integration
- Search functionality
- Book detail retrieval
- Missing cover fallback handling
- API reliability improvements with timeout and retry handling
- Cleaned API descriptions containing HTML markup
- Responsive frontend layouts
- Styled authentication pages
- Password visibility toggle
- Search input clear functionality
- Improved navigation with back-to-home buttons
- Dynamic quote fetch from a list of 50 quotes stored in `app/static/data/quotes.json`
- Dynamic homepage book carousel using Google Books API data
- Genre-based random book selection for homepage content
- Carousel navigation controls and slide indicators
- Responsive carousel layout adjustments
- Automatic carousel rotation with pause-on-hover behaviour
- Homepage genre grid with 24 curated genres linking to search results
- Corrected marketplace buy links on the book detail page

---

# Current Limitations

1. Authentication pages have been created, but registration and login logic are not yet connected.
2. Library and review functionality are not yet connected to the database.
3. Search autocomplete and filtering features are still planned.

---

# Key Design Decisions

1. Adopted the Flask application factory pattern early to avoid future restructuring.
2. Used environment variables to separate sensitive configuration from application code.
3. Used Flask Blueprints to keep routes organised.
4. Initialised SQLAlchemy early to allow database development alongside application development.
5. Separated API logic into `helpers.py` to keep routes clean.

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

The carousel also introduced reliability issues when retrieving random homepage books. Since the carousel depends on live Google Books API data, temporary API failures could result in no books being returned, causing the carousel content to appear empty.

Testing revealed that some requests returned *HTTP 503 Service Unavailable* responses from the Google Books API. When this occurred, the homepage received an empty book list instead of the expected featured books.

Additional issues were discovered during frontend testing:

- Carousel images used low-resolution API thumbnails, which caused quality issues when displayed at larger sizes.
- Responsive behaviour required adjustments across desktop, tablet, and mobile screen sizes.
- Carousel sizing required balancing image quality, layout space, and usability.
- Navigation controls and slide state management required JavaScript interaction to correctly switch between books.

### Solution

The random book generation system was improved by replacing random character searches with a predefined list of popular genres:

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

Added fallback handling inside `get_random_books()` by retrying the request with a different randomly selected genre when the first API request fails or returns no usable results.

This allows the homepage carousel to recover from temporary API failures while still safely returning an empty result if multiple attempts fail.

The carousel frontend was refined by:

- Adding responsive sizing adjustments using CSS media queries.
- Improving image display behaviour using object-fit styling.
- Adding fallback handling for missing book covers.
- Implementing JavaScript controls for previous and next navigation.
- Adding navigation indicators to show the active slide.
- Adding automatic slide rotation using `setInterval()`, resetting to the first slide at the end, with `mouseenter`/`mouseleave` pausing and resuming the timer.

Testing across different screen sizes highlighted the importance of designing components around real API data rather than placeholder content.

Also fixed a related inconsistency where `get_random_books()` was selecting from the full 50-genre list while the homepage genre grid used a curated 24-genre list. Aligned both to use the same curated list so the carousel only pulls from genres users can also browse directly.

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

The carousel occasionally failed to display a cover image. Some books returned by the Google Books API did not include available cover image data. This caused carousel slides to render without an image when no thumbnail was provided.

### Solution

Added fallback handling to use no-cover.png whenever a book did not contain a valid cover image.

```python
cover = book_info.get("imageLinks", {}).get("thumbnail", "/static/images/no-cover.png")
```

This complements the genre-based query change from Challenge 6, since genre searches tend to return more relevant, better-catalogued books that are more likely to have a cover image in the first place.

---

## Challenge 10: Blurry Carousel and Book Cover Thumbnails

### Challenge

Once images displayed correctly, thumbnails appeared visibly blurry when scaled up, particularly in the carousel.

### Solution

Google Books API image URLs often return lower-resolution thumbnails by default. Resolved by using a regular expression to rewrite the `zoom` parameter to a higher value (`zoom=3`) for a sharper source image, combined with CSS (`object-fit` and fixed carousel dimensions) to keep images from stretching awkwardly inside their containers.

---

# What Was Learned So Far

- Large refactors in Git can represent organised restructuring rather than major logic changes.
- Flask application factories provide better scalability than single-file applications.
- Environment variables help protect sensitive configuration.
- Database relationships require careful planning of keys and relationships.
- Flask-Migrate allows database changes without manually recreating tables.
- API keys should be rotated immediately if accidentally exposed.
- External APIs require validation because returned data may not always match expectations.
- API failures and empty results should be handled separately.
- Retry logic improves reliability when dealing with temporary failures.
- API data may require processing before displaying it to users.
- Python regular expressions can be used to clean unwanted HTML markup from external data.
- Frontend testing is important because issues may only appear after real API data is displayed.
- External API responses may require sanitisation before being shown to users.
- Responsive layouts need testing across multiple screen sizes, not only desktop.
- Reusable helper functions reduce duplicated API handling logic.
- Small UI features such as search clearing and password visibility improve usability.
- External API data often requires filtering and selection logic to create meaningful user experiences.
- Responsive components require testing with real content because API data can expose layout issues not visible with placeholders.
- Image quality and source resolution should be considered when designing media-heavy interfaces.
- Interactive components often require coordination between HTML, CSS, JavaScript, and backend data.
- Constructing third-party URLs requires the correct search path and query parameters, not just the domain and an identifier.
- UI state (such as active navigation indicators) needs to be explicitly synced with application state; it does not update automatically just because the underlying data changes.
- Not all API results include every expected field, so defensive access patterns (e.g. `.get()` with defaults) are necessary when consuming third-party data.

---

# Next Milestones

1. Implement authentication logic (registration, login, logout).
2. Connect User_Library functionality.
3. Implement reviews and ratings.
4. Add search improvements such as autocomplete and filtering.

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