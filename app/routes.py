from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required, logout_user
from app.helpers import search_books, get_book_details, get_random_books, FEATURED_GENRES
import re
from app import db, bcrypt
from app.models import Review, User, User_Library, Book

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
        
    saved = False 
    
    # Set library button state for logged-in users
    if current_user.is_authenticated:
        saved = User_Library.query.filter_by(user_id=current_user.id, google_book_id=book_id).first() is not None
    
    # Retrieve reviews for the book, ordered by date created in descending order
    reviews = Review.query.filter_by(google_book_id=book_id).order_by(Review.date_created.desc()).all()
    user_review = None
    
    # If the user is logged in, check if they have already submitted a review for this book
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(user_id=current_user.id, google_book_id=book_id).first()
    
    return render_template("book_detail.html", book=book, saved=saved, book_id=book_id, reviews=reviews, user_review=user_review)

@routes.route("/book/<book_id>/review", methods=["POST"])
@login_required
def create_or_update_review(book_id):
    
    # Get the rating and review text from the form submission
    rating = request.form.get("rating", type=int)
    review_text = request.form.get("review_text", "").strip() or None
    
    # Validate the rating to ensure it is between 1 and 5
    if not rating or rating < 1 or rating > 5:
        flash("Please provide a valid rating between 1 and 5.", "error")
        return redirect(url_for("routes.book_detail", book_id=book_id))
    
    # Ensure the book exists in the database before creating a review
    book = Book.query.filter_by(google_book_id=book_id).first()

    if not book:
        api_book = get_book_details(volume_id=book_id)

        if not api_book:
            flash("Unable to retrieve book details.", "error")
            return redirect(url_for("routes.book_detail", book_id=book_id))

        volume_info = api_book.get("volumeInfo", {})

        book = Book(
            google_book_id=book_id,
            title=volume_info.get("title", "Unknown Title"),
            authors=", ".join(volume_info.get("authors", [])),
            cover_image=volume_info.get("imageLinks", {}).get("thumbnail", "")
        )

        db.session.add(book)
        db.session.commit()
    
    # Check if the user has already submitted a review for this book
    existing = Review.query.filter_by(user_id=current_user.id, google_book_id=book_id).first()
    
    if existing:
        # Update the existing review
        existing.rating = rating
        existing.review_text = review_text
        flash("Your review has been updated.", "success")
    else:
        # Create a new review
        new_review = Review(user_id=current_user.id, google_book_id=book_id, rating=rating, review_text=review_text)
        db.session.add(new_review)
        flash("Your review has been submitted.", "success")
    
    db.session.commit()
    return redirect(url_for("routes.book_detail", book_id=book_id))

@routes.route("/book/<book_id>/review/delete", methods=["POST"])
@login_required
def delete_review(book_id):
    
    # Find the review submitted by the current user for the specified book
    review = Review.query.filter_by(user_id=current_user.id, google_book_id=book_id).first()
    
    if review:
        # If the review exists, delete it from the database
        db.session.delete(review)
        db.session.commit()
        flash("Your review has been deleted.", "success")
    else:
        flash("No review found to delete.", "error")
    
    return redirect(url_for("routes.book_detail", book_id=book_id))


# ABOUT
@routes.route("/about")
def about():
    return render_template("about.html")

# LIBRARY
@routes.route("/library/add/<book_id>", methods=["POST"])
@login_required
def add_to_library(book_id):
    
    # Check if the book already exists in the database
    book = Book.query.filter_by(google_book_id=book_id).first()
    
    # If the book doesn't exist, fetch its details from the Google Books API and add it to the database
    if not book:
        api_book = get_book_details(volume_id=book_id)
    
        if not api_book:
            flash("Unable to retrieve book details.", "error")
            return redirect(request.referrer or url_for("routes.your_library"))
        
        volume_info = api_book.get("volumeInfo", {})
        
        # Safely extract and clean HTML tags from book description
        book = Book(google_book_id=book_id,
                    title=volume_info.get("title", "Unknown Title"),
                    authors=", ".join(volume_info.get("authors", [])),
                    cover_image=volume_info.get("imageLinks", {}).get("thumbnail", "")
        )
        
        db.session.add(book)
        db.session.commit()
    
    # Check if the book is already in the user's library
    existing = User_Library.query.filter_by(user_id=current_user.id, google_book_id=book_id).first()
    
    if existing:
        flash("Book is already in your library.", "error")
    
    # If the book is not already in the library, add it
    else:
        saved_book = User_Library(user_id=current_user.id, google_book_id=book_id)
        
        db.session.add(saved_book)
        db.session.commit()
        
        flash("Book added to your library!", "success")
    
    return redirect(request.referrer or url_for("routes.your_library"))

@routes.route("/library/remove/<book_id>", methods=["POST"])
@login_required
def remove_from_library(book_id):
    # Find the book in the user's library
    book = User_Library.query.filter_by(user_id=current_user.id, google_book_id=book_id).first()
    
    # If the book exists in the library, remove it
    if book:
        db.session.delete(book)
        db.session.commit()
        flash("Book removed from your library!", "success")
    
    return redirect(request.referrer or url_for("routes.your_library"))

@routes.route("/library")
@login_required
def your_library():

    # Retrieve all books in the user's library
    library_entries = User_Library.query.filter_by(user_id=current_user.id).all()

    # Extract the book details for each entry in the user's library
    books = [entry.book for entry in library_entries]
    
    total = User_Library.query.filter_by(user_id=current_user.id).count()

    return render_template("your_library.html", books=books, library_entries=library_entries, total=total)

@routes.route("/library/delete", methods=["POST"])
@login_required
def delete_user():
    
    # Get the password from the form submission and verify it against the current user's password hash
    password = (request.form.get("password") or "").strip()
    
    if not bcrypt.check_password_hash(current_user.password_hash, password):
        flash("Incorrect password. Please try again.", "error")
        return redirect(url_for("routes.your_library"))
    
    # Delete the user account and log the user out
    user = User.query.get(current_user.id)
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash("Your account has been deleted.", "success")
    return redirect(url_for("routes.index"))
    