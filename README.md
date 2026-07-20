# BiblioTech

BiblioTech is a full-stack Flask web application that allows users to discover books using the Google Books API, build a personal library, write reviews, and manage their account.

The application uses PostgreSQL for persistent storage and follows the Flask application factory pattern with Blueprints for maintainability and scalability.

---

# Site Logo

![BiblioTech Logo](app/static/images/BiblioTech_Logo.png)

---

## Application Link

### Live Site: [BiblioTech](https://bibliotech-ifum.onrender.com)

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

## Key Skills Demonstrated

- Flask application factory pattern
- Blueprints and modular routing
- REST API integration
- PostgreSQL relational database design
- SQLAlchemy ORM
- Database migrations with Flask-Migrate
- Authentication and session management
- CRUD operations
- Password hashing with Flask-Bcrypt
- Responsive frontend development

---

## Features

Authentication
- Register
- Login
- Logout
- Secure password hashing

Book Discovery
- Search
- Live search suggestions with autocomplete
- Pagination
- Book details
- Genre-based browsing
- Homepage genre-based book carousel

Personal Library
- Save books
- Remove books
- View saved book collection
- Track when books were added

Reviews
- Ratings
- Edit
- Delete

Account
- Delete account with password confirmation
- Preserve reviews after account deletion

---

## Homepage Features

- Dynamic quote section
- Google Books powered carousel
- Genre-based random book recommendations
- Automatic carousel rotation with navigation controls
- Fallback handling for missing book covers
- Genre grid linking directly to search results

---

## Review Features

- Authenticated users can leave a 1-5 star rating and optional written review.
- Users can edit or delete their own reviews.
- Reviews are displayed on book detail pages for all visitors.
- Database constraints prevent duplicate reviews from the same user on the same book.
- Reviews are preserved after account deletion and displayed as belonging to a deleted user.

---

## Architecture

The project follows the Flask application factory pattern.

- Blueprints separate authentication and main application routes.
- SQLAlchemy manages database models.
- Helper functions encapsulate Google Books API interactions.
- Flask-Migrate manages schema migrations.
- Flask-Login handles authentication.

---

## Project Structure

```text
BiblioTech/
│
├── migrations/
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

- `app/routes.py` → main pages (`/`, `/search-results`, `/book/<book_id>`, `/book/<book_id>/review`, `/library`, `/library/delete`, `/genre/<subject>`, `/about`)
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
| `/auto-complete`  | Search Autocomplete |
| `/book/<book_id>` | Book details |
| `/book/<book_id>/review` | Create or update review |
| `/book/<book_id>/review/delete` | Delete review |
| `/library` | Personal library |
| `/library/add/<book_id>` | Add book to personal library |
| `/library/remove/<book_id>` | Remove book from personal library |
| `/genre/<subject>` | Browse books by genre |
| `/library/delete` | Delete user account |
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

### Your Library

![Your Library](app/static/images/Your_Library.png)

### Book Detail Reviews

![Book Detail Reviews](app/static/images/Reviews.png)

### More Like This

![More Like This](app/static/images/Recommend.png)