# BiblioTech

BiblioTech is a Flask-based book discovery application. The project has been refactored to an app factory + package structure and is set up for PostgreSQL via Flask-SQLAlchemy.

## Current Status

The codebase currently includes:
- App factory setup with blueprint registration
- Environment-based configuration
- SQLAlchemy initialization
- Scaffolded routes and templates for core pages
- Flask-Migrate configured
- Initial database schema created
- PostgreSQL database connected
- Google Books API integration for book searching and book detail retrieval

The application now supports querying books through the Google Books API and displaying search results and individual book details.

Additional features, including authentication, personal library functionality, and reviews, are still being implemented.

The database models have been designed and the initial migration has been successfully applied using Flask-Migrate.

## Project Structure

```text
BiblioTech/
  run.py
  Procfile
  requirements.txt
  app/
     __init__.py
     config.py
     models.py
     routes.py
     helpers.py
     templates/
     static/
  data/
  docs/
```

## Setup

1. Open a terminal in the `BiblioTech` folder.
2. Activate the virtual environment:
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
   - Command Prompt: `.\.venv\Scripts\activate.bat`
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional but recommended) set environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL`

5. Apply the database migrations:

```bash
python -m flask db upgrade
```

For hosted PostgreSQL (for example Render), ensure your `DATABASE_URL` includes `sslmode=require`.

## Run

Local development:

```bash
python run.py
```

Gunicorn deployment:

```bash
gunicorn run:app
```

For database management commands:

```bash
python -m flask db <command>
```

## Implemented Routes

- `/` → Home (`index.html`)
- `/search` → Query-driven book search using Google Books API (`search_results.html`)
- `/book/<book_id>` → Book detail view using API book information (`book_detail.html`)
- `/library` → Your library (`your_library.html`)
- `/about` → About (`about.html`)
- `/auth/login` → Login (`auth/login.html`)
- `/auth/signup` → Sign up (`auth/signup.html`)
- `/auth/logout` → Clear session and redirect to login

## Documentation

- Planning: [docs/Planning.md](docs/Planning.md)
- Documentation: [docs/BiblioTech-Documentation.md](docs/BiblioTech-Documentation.md)