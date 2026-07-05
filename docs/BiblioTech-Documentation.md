# BiblioTech Documentation

**Last updated:** July 5, 2026

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

This was valid for early development but harder to scale.

### 2. Migration to package-based structure
The project was refactored into a package layout:
- run.py
- app/__init__.py
- app/config.py
- app/models.py
- app/routes.py
- app/templates/
- app/static/

This aligns with Flask best practices and is easier to maintain for larger features.

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

At this stage, routes are scaffolded and mostly template-rendering placeholders.

---

## Frontend Status

### Templates
Current templates are in `app/templates/` and use Jinja inheritance via `base.html`.

Pages are present for:
- home
- search results
- book detail
- library
- login
- signup
- about (template file exists)

### Static assets
Current static files are in `app/static/`:
- CSS with global reset and header/background styling
- JS file present but currently empty
- image assets present for branding/background

---

## Database and Models Status

- SQLAlchemy is initialized in app setup.
- `app/models.py` exists but currently has no model classes yet.
- No migrations are configured yet.

This means the database layer is prepared structurally, but domain tables (Users, Books, Reviews, Library) still need implementation.

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
- foundational Flask app architecture
- routing skeleton
- template structure
- deployment entrypoint configured
- environment-based config + SQLAlchemy initialization

---

## Current Limitations

1. API integration is not yet implemented in routes.
2. Models are not yet defined in `app/models.py`.
3. Auth routes are placeholders (forms/logic not implemented yet).
4. Several pages are scaffolded headings rather than feature-complete views.
5. README run instructions may still reference the old `app.py` entrypoint and should be synchronized with current structure.

---

## Key Design Decisions

1. Move to app factory pattern early to avoid future structural debt.
2. Keep config environment-driven to support local and deployed environments.
3. Separate route registration via blueprint for modular growth.
4. Initialize SQLAlchemy now so model development can begin without more architecture changes.

---

## Setup and Run (Current Structure)

1. Create/activate virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Set environment variables as needed:
   - `SECRET_KEY`
   - `DATABASE_URL`
4. Run locally:
   - `python run.py`
5. Deploy command:
   - `gunicorn run:app`

---

## What Was Learned So Far

- Structural refactors can look large in Git but still represent organized file moves.
- Flask app factory structure is cleaner for medium/large projects than flat single-file layouts.
- Environment-variable-based config is necessary for secure deployments.
- Wiring SQLAlchemy early helps prepare for model implementation even before tables are defined.

---

## Next Milestones

1. Implement `app/models.py` with initial schema.
2. Add DB creation/migration workflow.
3. Implement Google Books API helper module and route integration.
4. Complete auth flow (signup, login, logout, route protection).
5. Build out search results and book detail with real API data.
6. Add review and library persistence.
7. Fix and wire `about` page template/route.

---

## References

- Flask documentation: https://flask.palletsprojects.com/
- Flask SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- Flask App Structure: https://www.colabcodes.com/post/flask-application-structure-organizing-python-web-apps-for-scalability
- Gunicorn docs: https://docs.gunicorn.org/
- Google Books API: https://developers.google.com/books/docs/v1/using
