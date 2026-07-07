# BiblioTech Documentation

**Last updated:** July 7, 2026

---

## Overview

BiblioTech is a Flask-based book discovery web application designed to support searching and exploring books, then extending into user accounts, reviews, and personal library features.

The long-term product direction is powered by the Google Books API, while the current codebase has already been restructured into a scalable Flask app factory layout.

---

## Project Development Summary

### 1. Initial structure (flat Flask layout)

The project initially used a flat file structure at repository root:

- app.py
- routes.py
- config.py
- models.py
- templates/
- static/

This was valid for early development but became harder to maintain as more features were planned.

### 2. Migration to package-based structure

The project was refactored into a package layout:

- run.py
- app/__init__.py
- app/config.py
- app/models.py
- app/routes.py
- app/helpers.py
- app/templates/
- app/static/

This follows Flask best practices and provides a better structure for future development.

### 3. Runtime and deployment updates

Deployment was updated to use the new entrypoint pattern:

- Procfile: `web: gunicorn run:app`

Local startup now uses:

- `python run.py`

---

## Current Architecture

### App factory

`app/__init__.py` defines:

- Flask app creation
- config loading from `Config`
- SQLAlchemy initialization (`db.init_app(app)`)
- blueprint registration for routes

### Configuration

`app/config.py` currently provides:

- `SECRET_KEY` from environment variable
- `SQLALCHEMY_DATABASE_URI` from `DATABASE_URL`
- `SQLALCHEMY_TRACK_MODIFICATIONS = False`

### Entry point

`run.py` imports `create_app()` and runs the application using environment-based configuration. Debug mode is disabled when running in production.

---

## Current Implemented Pages and Routes

`app/routes.py` currently provides page-render routes:

- `/` -> Home (`index.html`)
- `/search` -> Search results (`search_results.html`)
- `/book/<book_id>` -> Book detail (`book_detail.html`)
- `/library` -> Your Library (`your_library.html`)
- `/auth/login` -> Login (`auth/login.html`)
- `/auth/signup` -> Sign up (`auth/signup.html`)
- `/auth/logout` -> Clears session and redirects to login

At this stage, some routes remain structural placeholders. The `/search` route is fully connected to live Google Books API data via `helpers.py`, and the `/book/<book_id>` route retrieves book details from the API.

---

## Frontend Status

### Templates

Current templates are in `app/templates/` and use Jinja inheritance through `base.html`.

Pages are present for:

- home
- search results with live Google Books API data
- book detail with API book information
- Your library
- login
- signup
- about

### Static assets

Current static files are in `app/static/`:

- CSS with global reset and header/background styling
- JS file present but currently empty
- image assets present for branding/background
- default book cover image for books without available thumbnails

---

## Database and Models Status

SQLAlchemy and Flask-Migrate are configured through the application factory.

The initial database migration has been generated and applied successfully.

Current models implemented:

- User
- Book
- User_Library
- Review

### User

Stores registered users with:

- id
- username
- password_hash
- date_created

### Book

Stores Google Books API book information:

- google_book_id (Primary Key)
- title
- authors
- cover_image
- buy_links
- date_created

### User_Library

Represents the relationship between a user and their saved books.

Composite Primary Key:

- user_id
- google_book_id

Additional field:

- date_created

### Review

Stores user reviews for books.

Fields:

- review_id (Primary Key)
- user_id (Foreign Key)
- google_book_id (Foreign Key)
- rating
- review_text
- date_created

The database now contains the required tables:

- users
- books
- user_library
- reviews

---

## Planned Features vs Current State

### Planned (from project plan)

- search autocomplete
- homepage quote + carousel
- genre filters
- user authentication and protected library
- reviews/ratings
- full database schema (Users, Books, User_Library, Reviews)

### Current implemented state

- Flask application factory architecture
- Blueprint routing structure
- SQLAlchemy configured
- Flask-Migrate configured
- Database schema created
- Core model classes implemented
- Initial migration completed
- Deployment entrypoint configured
- Environment-based configuration
- Google Books API integration (`helpers.py`)
- Search results connected to live API data
- Book detail retrieval using Google Books API
- Default cover handling for books without available thumbnails

---

## Current Limitations

1. Authentication logic is still to be implemented.
2. Library and review functionality have not yet been connected to the database.

---

## Key Design Decisions

1. Move to app factory pattern early to avoid restructuring later.
2. Keep configuration environment-driven to support local and deployed environments.
3. Separate routes using blueprints for easier organisation.
4. Initialise SQLAlchemy early so database development could begin before implementing application features.
5. Separate API request logic into `helpers.py` to keep routes cleaner.

---

## Helpers (API Integration)

- `fetch_json(params)` — Centralised request handler. Sends params to Google Books API, handles errors (timeouts, bad responses, JSON parse failures), returns parsed JSON or None.
- `search_books(query, max_results, start_index, order_by)` — Search by title, author, or keyword. Used by `/search` route.
- `get_book_details(volume_id)` — Fetch single book details. Used by `/book/<book_id>` route.
- `get_random_books(count)` — Random books for homepage carousel. Picks random letter + random startIndex to avoid seeding issues.

Cover fallback handling provides a default image when Google Books API does not return a thumbnail.

**Key caveat:** Google Books API quota is 1,000 requests/day free tier. Each page load = 1 request.

**References:**

- [Google Books API docs](https://developers.google.com/books/docs/v1/using)
- Pattern reused from GlobalGrub helpers architecture

---

## Challenges Faced and Solutions

### Challenge 1: Redesigning the Entity Relationship Diagram (ERD)

**Challenge**

My original ERD no longer reflected the structure of the application as the project developed. Some relationships and keys needed to be redesigned.

**Solution**

I researched database design tools and found DBdiagram.io. Using this, I recreated the ERD, which helped me visualise the relationships between tables and understand where composite primary keys and foreign keys were required before implementing the models.

---

### Challenge 2: Learning Flask-Migrate

**Challenge**

I had not previously used Flask-Migrate, so understanding how it fitted into the project required additional research.

Another challenge was that Flask CLI commands such as `flask db migrate` and `flask db upgrade` were not recognised directly in the terminal.

**Solution**

I installed Flask-Migrate and configured it within the Flask application factory.

The CLI issue was resolved by running Flask commands through Python instead:

- `python -m flask db init`
- `python -m flask db migrate -m "initial migration"`
- `python -m flask db upgrade`

This allowed the commands to run using the correct Python environment.

---

### Challenge 3: Designing the Database Models

**Challenge**

Designing the database models required understanding how tables connected and deciding which fields should be primary keys, foreign keys, or normal columns.

**Solution**

I worked through each model individually, researched SQLAlchemy where necessary, and refined the structure until it matched the application's requirements.

---

### Challenge 4: Refactoring the Project Structure

**Challenge**

The project originally used a simple Flask structure, but this became harder to manage as more features were planned.

**Solution**

I reorganised the project into a Flask application factory structure using an `app` package, separating configuration, models, routes, templates and static files into a more scalable layout.

---

### Challenge 5: Integrating the Google Books API

**Challenge**

Building the API integration layer (`helpers.py`) required connecting several new concepts at once — external requests, error handling, and environment variables. I also accidentally exposed my live API key by pasting a request URL that included it.

**Solution**

I structured `helpers.py` using the same pattern as my GlobalGrub project, with a shared `fetch_json()` function for error handling and smaller functions built on top for specific needs. When the API key was exposed, I regenerated it through Google Cloud Console and confirmed `.env` was excluded via `.gitignore` before continuing.

---

## What Was Learned So Far

- Structural refactors can look large in Git but still represent organised file changes rather than major logic changes.
- Flask app factory structure is cleaner for medium and larger projects than a flat single-file layout.
- Environment variables help keep sensitive configuration separate from the code.
- SQLAlchemy models represent database tables.
- Foreign keys connect related tables together.
- Composite primary keys can enforce uniqueness in relationship tables such as User_Library.
- Flask-Migrate manages database changes without manually recreating tables.
- API keys must be rotated immediately if accidentally exposed, even in local testing.
- Renaming a function requires updating every file that imports it, or Python raises an `ImportError`.
- Editor warnings (e.g. Pylance) don't always mean broken code — sometimes it's just interpreter configuration.
- External API integration requires handling failures and missing data gracefully.

---

## Next Milestones

1. Implement user authentication (registration, login and logout).
2. Connect User_Library functionality.
3. Implement review submission and retrieval.

---

## References

- Flask documentation: https://flask.palletsprojects.com/
- Flask SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- Flask App Structure: https://www.colabcodes.com/post/flask-application-structure-organizing-python-web-apps-for-scalability
- Flask Migrate documentation: https://flask-migrate.readthedocs.io/en/latest/
- Gunicorn docs: https://docs.gunicorn.org/
- Google Books API: https://developers.google.com/books/docs/v1/using
- DBdiagram.io: https://dbdiagram.io/
- python-dotenv: https://pypi.org/project/python-dotenv/
- Requests library: https://requests.readthedocs.io/