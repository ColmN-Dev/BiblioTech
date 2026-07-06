# BiblioTech Documentation

**Last updated:** July 6, 2026

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

`run.py` imports `create_app()` and runs the app in debug mode for local development.

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

At this stage, routes are implemented as structural placeholders and mainly render templates without full backend logic or API integration.

---

## Frontend Status

### Templates

Current templates are in `app/templates/` and use Jinja inheritance through `base.html`.

Pages are present for:

- home
- search results
- book detail
- Your library
- login
- signup
- about

### Static assets

Current static files are in `app/static/`:

- CSS with global reset and header/background styling
- JS file present but currently empty
- image assets present for branding/background

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

- Google Books API integration
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

---

## Current Limitations

1. Google Books API integration has not yet been connected.
2. Authentication logic is still to be implemented.
3. Search functionality is currently scaffolded.
4. Library and review functionality have not yet been connected to the database.

---

## Key Design Decisions

1. Move to app factory pattern early to avoid restructuring later.
2. Keep configuration environment-driven to support local and deployed environments.
3. Separate routes using blueprints for easier organisation.
4. Initialise SQLAlchemy early so database development could begin before implementing application features.

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

## What Was Learned So Far

- Structural refactors can look large in Git but still represent organised file changes rather than major logic changes.
- Flask app factory structure is cleaner for medium and larger projects than a flat single-file layout.
- Environment variables help keep sensitive configuration separate from the code.
- SQLAlchemy models represent database tables.
- Foreign keys connect related tables together.
- Composite primary keys can enforce uniqueness in relationship tables such as User_Library.
- Flask-Migrate manages database changes without manually recreating tables.

---

## Next Milestones

1. Implement user authentication (registration, login and logout).
2. Integrate the Google Books API.
3. Connect search results to live API data.
4. Implement book detail pages using API responses.
5. Connect User_Library functionality.
6. Implement review submission and retrieval.

---

## References

- Flask documentation: https://flask.palletsprojects.com/
- Flask SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- Flask App Structure: https://www.colabcodes.com/post/flask-application-structure-organizing-python-web-apps-for-scalability
- Flask Migrate documentation: https://flask-migrate.readthedocs.io/en/latest/
- Gunicorn docs: https://docs.gunicorn.org/
- Google Books API: https://developers.google.com/books/docs/v1/using