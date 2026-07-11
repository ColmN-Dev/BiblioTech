from flask import Blueprint, render_template, redirect, request, url_for, session
from app.helpers import search_books, get_book_details, get_random_books, FEATURED_GENRES
import re 

routes = Blueprint("routes", __name__)


# INDEX
@routes.route("/")
def index():
    
    featured_books = get_random_books(5) or []
    
    return render_template("index.html", featured_books=featured_books, genres=FEATURED_GENRES)


# SEARCH
@routes.route("/search-results")
def search_results():
    """If the search query is empty, redirect to the home page. Otherwise, render the search results page with the query."""
    query = request.args.get("query", "").strip()
    
    if not query:
        return redirect(url_for("routes.index"))
    
    results = search_books(query)
    
    if results is None:
        # Handle the case where the API request failed
        return render_template("search_results.html", query=query, results=[], error="Failed to fetch search results. Please try again later.")
    
    return render_template("search_results.html", query=query, results=results)


# BOOK DETAIL
@routes.route("/book/<book_id>")
def book_detail(book_id):
    
    book = get_book_details(volume_id=book_id)
    
    if not book:
        return redirect(url_for("routes.index"))
    
    # Safely extract and clean HTML tags from book description
    volume_info = book.setdefault("volumeInfo", {})
    volume_info.setdefault("customLinks", {})
    description = volume_info.get("description")

    if description:
        volume_info["description"] = re.sub(r"<.*?>", "", description)
    
    return render_template("book_detail.html", book=book)


# LIBRARY
@routes.route("/library")
def your_library():
    return render_template("your_library.html")


# ABOUT
@routes.route("/about")
def about():
    return render_template("about.html")


# AUTH - SIGNUP
@routes.route("/auth/signup", methods=["GET", "POST"])
def signup():
    return render_template("auth/signup.html")

# AUTH - LOGIN
@routes.route("/auth/login", methods=["GET", "POST"])
def login():
    return render_template("auth/login.html")


# AUTH - LOGOUT
@routes.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("routes.login"))
