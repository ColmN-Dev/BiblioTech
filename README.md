# BiblioTech

BiblioTech is a Flask-based book discovery application. The project has been refactored into a Flask application factory + package structure and uses PostgreSQL through Flask-SQLAlchemy.

The application uses the Google Books API to allow users to search for books, view book details, and explore available book information.

## Current Status

The codebase currently includes:

- Flask application factory setup with blueprint registration
- Environment-based configuration
- SQLAlchemy initialization
- PostgreSQL database connection
- Flask-Migrate configuration
- Initial database schema and migrations
- Google Books API integration
- Centralised API request handling with timeout, retry support, and fallback handling
- Search functionality
- Book detail pages
- Dynamic homepage quote section
- Google Books powered homepage carousel
- Genre-based random book selection for homepage content
- Carousel navigation controls, active indicators, and auto-rotation
- Responsive frontend layouts
- Styled authentication pages
- Password visibility toggle
- Search input clearing functionality

Additional features, including authentication logic, personal library functionality, and reviews, are still being implemented.

The database models have been designed and the initial migration has been successfully applied using Flask-Migrate.

---

---

## Homepage Features

The homepage currently includes dynamic content powered by external data sources.

Features include:

- Rotating quote section using local JSON data
- Google Books API powered carousel
- Random book selection based on popular genres
- Previous and next navigation controls
- Active slide indicators
- Automatic carousel rotation with pause-on-hover behaviour
- Missing cover image fallback handling

---

## Project Structure

```text
BiblioTech/
│
├── run.py
├── Procfile
├── requirements.txt
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── helpers.py
│   │
│   ├── templates/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── data/
│           └── quotes.json
│
└── docs/
```

---

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

---

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

