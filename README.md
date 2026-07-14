# BiblioTech

BiblioTech is a Flask-based book discovery application. The project has been refactored into a Flask application factory + package structure and uses PostgreSQL through Flask-SQLAlchemy.

The application uses the Google Books API to allow users to search for books, view book details, and explore available book information.

---

## Technologies Used

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-Bcrypt
- Google Books API
- HTML
- CSS
- JavaScript

---

## Features

BiblioTech currently includes:

- Flask application factory architecture with Blueprints
- PostgreSQL integration using Flask-SQLAlchemy and Flask-Migrate
- Google Books API integration with timeout handling, retries, and fallback behaviour
- Book search with pagination
- Individual book detail pages
- User authentication with Flask-Login and Flask-Bcrypt
- Personal library CRUD functionality (save, view, and remove books)
- Responsive homepage with dynamic quotes, genre browsing, and Google Books carousel
- Mobile-friendly responsive interface with improved navigation

Future development will focus on user reviews, ratings, and enhanced search functionality.

---

## Homepage Features

- Dynamic quote section
- Google Books powered carousel
- Genre-based random book recommendations
- Automatic carousel rotation with navigation controls
- Fallback handling for missing book covers
- Genre grid linking directly to search results

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
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
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
---

## Routing Structure

- `app/routes.py` → main pages (`/`, `/search-results`, `/book/<book_id>`, `/library`, `/about`)
- `app/auth/routes.py` → auth routes (`/auth/login`, `/auth/signup`, `/auth/logout`)
- `app/auth/__init__.py` → auth blueprint setup

Template links and redirects for authentication use blueprint-qualified endpoints:

- `url_for('auth.login')`
- `url_for('auth.signup')`
- `url_for('auth.logout')`

---

## Implemented Routes

| Route | Purpose |
|-------|---------|
| `/` | Homepage |
| `/search-results` | Search books |
| `/book/<book_id>` | Book details |
| `/library` | Personal library |
| `/about` | About page |
| `/auth/login` | Login |
| `/auth/signup` | Register |
| `/auth/logout` | Logout |

---

## Documentation

- Planning: [docs/Planning.md](docs/Planning.md)
- Documentation: [docs/BiblioTech-Documentation.md](docs/BiblioTech-Documentation.md)

---

## Screenshots

### Homepage 

![Homepage](app/static/images/Homepage.png)

### Your Library - Light Mode

![Your Library](app/static/images/Your_Library.png)