from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required
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
    page = request.args.get("page", 1, type=int)
    
    if not query:
        return redirect(url_for("routes.index"))
    
    # Set the number of results per page and calculate the start index for pagination
    per_page = 20
    start_index = (page - 1) * per_page

    # Step back until we land on a page with results, or page 1 if nothing exists.
    results = search_books(query, max_results=per_page, start_index=start_index)
    while page > 1 and not results:
        page -= 1
        start_index = (page - 1) * per_page
        results = search_books(query, max_results=per_page, start_index=start_index)
    
    return render_template("search_results.html", query=query, results=results, page=page, per_page=per_page)


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


# ABOUT
@routes.route("/about")
def about():
    return render_template("about.html")

# LIBRARY
@routes.route("/library")
@login_required
def your_library():
    return render_template("your_library.html")