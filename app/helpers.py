# -----------------------------
# IMPORTS
# -----------------------------

import logging
import os
import random
import time

import requests
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Book


# Used for tracking errors without printing everything to the console
logger = logging.getLogger(__name__)


# Load environment variables from .env
load_dotenv()


# -----------------------------
# API CONFIGURATION
# -----------------------------

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# API key is stored outside the code for security
API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")


# -----------------------------
# CACHE SETTINGS
# -----------------------------

# Keep API results for 6 hours
API_CACHE_DURATION = 21600

# Keep homepage carousel for 6 hours
HOMEPAGE_CACHE_DURATION = 21600


# Prevent memory cache becoming too large
API_CACHE_MAX_SIZE = 200


# Stores API responses while the Flask app is running
# cache_key -> (time_saved, response_data)
_cache = {}

# Stores books by subject:
_subject_cache = {}


# Stores homepage carousel separately
_homepage_cache = None
_homepage_cache_time = None


# -----------------------------
# HOMEPAGE GENRES
# -----------------------------

FEATURED_GENRES = [
    "Fiction",
    "Fantasy",
    "Science Fiction",
    "Mystery",
    "Thriller",
    "Romance",
    "Horror",
    "Crime",
    "Adventure",
    "Biography",
    "History",
    "Science",
    "Technology",
    "Business",
    "Self Help",
    "Psychology",
    "Philosophy",
    "Poetry",
    "Classics",
    "Drama",
    "Travel",
    "Cooking",
    "Young Adult",
    "Comics",
]


# -----------------------------
# BOOK HELPER FUNCTIONS
# -----------------------------


def get_preferred_isbn(book):
    """
    Returns the best ISBN available for a book.

    Uses ISBN-13 first because it is the modern standard.
    Falls back to ISBN-10 if ISBN-13 does not exist.
    """

    if not book:
        return None

    volume_info = book.get("volumeInfo", {})

    identifiers = volume_info.get(
        "industryIdentifiers",
        []
    )

    isbn_10 = None

    for item in identifiers:

        isbn_type = item.get("type")
        isbn = item.get("identifier")


        if not isbn:
            continue


        # Remove spaces and hyphens
        isbn = isbn.replace("-", "").replace(" ", "")


        if isbn_type == "ISBN_13":
            return isbn


        if isbn_type == "ISBN_10":
            isbn_10 = isbn


    return isbn_10



def has_isbn(book):
    """
    Checks whether a book has an ISBN.

    ISBN is needed for external links
    and Open Library covers.
    """

    return get_preferred_isbn(book) is not None



def has_cover(book):
    """
    Checks whether Google Books provides a cover image.
    """

    if not book:
        return False


    volume_info = book.get(
        "volumeInfo",
        {}
    )


    return bool(
        volume_info.get("imageLinks")
    )



def add_custom_links(book):
    """
    Adds external book links.

    Creates links for:
    - Amazon
    - Goodreads
    - WorldCat
    """

    if not book or "volumeInfo" not in book:
        return book


    volume_info = book["volumeInfo"]

    isbn = get_preferred_isbn(book)


    # Always create the dictionary so templates can safely access it
    volume_info["customLinks"] = {}


    if isbn:

        volume_info["customLinks"] = {
            "amazon": f"https://www.amazon.com/s?k={isbn}",
            "goodreads": f"https://www.goodreads.com/search?q={isbn}",
            "worldcat": f"https://search.worldcat.org/search?q={isbn}",
        }


    return book



def add_openlibrary_cover(book):
    """
    Creates an Open Library cover URL using ISBN.

    Used as a fallback if Google has no cover.
    """

    if not book:
        return book


    volume_info = book.get(
        "volumeInfo",
        {}
    )


    isbn = get_preferred_isbn(book)


    if isbn:

        volume_info["openLibraryFallbackCover"] = (
            f"https://covers.openlibrary.org/isbn/{isbn}-L.jpg"
        )


    return book



def prepare_book(book):
    """
    Cleans and prepares a Google Books result.

    Adds:
    - external links
    - fallback cover
    - final display cover
    """

    book = add_custom_links(book)
    book = add_openlibrary_cover(book)

    volume_info = book.get("volumeInfo", {})


    # Google cover
    google_cover = (
        volume_info
        .get("imageLinks", {})
        .get("thumbnail")
    )
    
    if google_cover:
        google_cover = google_cover.replace("http://", "https://")
        google_cover = google_cover.replace("&edge=curl", "")
        google_cover = google_cover.replace("&zoom=1", "&zoom=3")


    # Open Library fallback cover
    openlibrary_cover = volume_info.get(
        "openLibraryFallbackCover"
    )

    volume_info["googleCover"] = google_cover
    volume_info["openLibraryCover"] = openlibrary_cover
    
    volume_info["displayCover"] = google_cover or openlibrary_cover

    if not volume_info["displayCover"]:
        logger.info(
            f"No cover available for '{volume_info.get('title')}'"
        )


    return book

# -----------------------------
# GOOGLE BOOKS API FUNCTIONS
# -----------------------------


def fetch_json(params, url=BASE_URL):
    """
    Sends a request to Google Books API.

    Uses:
    - cache to avoid repeated requests
    - retries for temporary API errors
    """
    
    # Create a unique name for this request
    cache_key = str(sorted(params.items())) + url


    # Check if this request was already cached
    if cache_key in _cache:

        saved_time, data = _cache[cache_key]

        # Return cached data if it is still valid
        if time.time() - saved_time < API_CACHE_DURATION:
            return data


    # Stop if API key is missing
    if not API_KEY:

        logger.warning(
            "Google Books API key is missing."
        )

        return None


    # Try the request 3 times
    for attempt in range(3):

        try:

            response = requests.get(
                url,
                params={
                    **params,
                    "key": API_KEY
                },
                timeout=30
            )


            response.raise_for_status()


            data = response.json()

            # Save successful results
            _cache[cache_key] = (
                time.time(),
                data
            )


            # Prevent cache growing forever
            if len(_cache) > API_CACHE_MAX_SIZE:
                _cache.clear()


            return data


        except requests.RequestException as error:
            

            status_code = "No response"


            if error.response:

                status_code = error.response.status_code

            logger.warning(
                f"Google API error: {status_code}, attempt {attempt + 1}"
            )


            # Stop retrying if quota is exceeded
            if status_code == 429:
                break


            # Wait longer after each failed attempt
            time.sleep(2 ** attempt)



    # Return nothing if all attempts fail
    return None



# -----------------------------
# SEARCH FUNCTIONS
# -----------------------------


def search_books(query, max_results=20, start_index=0):
    """
    Searches Google Books and prepares results.
    """

    data = fetch_json({

        "q": query,
        "maxResults": max_results,
        "startIndex": start_index,
        "printType": "books"

    })


    if not data or "items" not in data:

        logger.warning(
            f"No results for search: {query}"
        )
        
        return []

    logger.info(f"Google returned {len(data['items'])} books for {query}")


    books = []


    for book in data["items"]:

        books.append(
            prepare_book(book)
        )


    return books



def get_book_details(volume_id):
    """
    Gets one specific book using its Google ID.
    """

    data = fetch_json(
        {},
        url=f"{BASE_URL}/{volume_id}"
    )


    if not data:

        return None


    return prepare_book(data)



# -----------------------------
# BOOKS BY SUBJECT / CATEGORY
# -----------------------------


def get_books_by_subject(subject):
    """
    Gets books by subject or category.
    Creates a cache so the same subject is not requested repeatedly from the API.
    """
    
    if not subject:
        return []

    # Check if the subject is already cached
    global _subject_cache
    
    if subject in _subject_cache:
        return _subject_cache[subject]

    data = fetch_json({
        "q": subject,
        "maxResults": 20,
        "printType": "books"
    })

    if not data or "items" not in data:
        return _subject_cache.get(subject, [])

    books = []

    for book in data["items"]:
        books.append(prepare_book(book))

    # Cache the results for this subject
    _subject_cache[subject] = books

    return books

# -----------------------------
# HOMEPAGE CAROUSEL
# -----------------------------


def get_random_books(count=5):
    """
    Gets random books for the homepage carousel.

    Uses cache so the homepage does not
    request new books every time.
    """

    global _homepage_cache
    global _homepage_cache_time


    # Return cached carousel if still valid
    if _homepage_cache and _homepage_cache_time:

        cache_age = (
            time.time() - _homepage_cache_time
        )


        if cache_age < HOMEPAGE_CACHE_DURATION:

            return _homepage_cache



    # Try different genres if one fails
    for _ in range(3):


        genre = random.choice(FEATURED_GENRES)
        
        data = fetch_json({

            "q": genre,
            "maxResults": 10,
            "printType": "books"

        })


        if not data or "items" not in data:

            continue

        books = []


        for book in data["items"]:
        
            

            # Only use books with covers
            if has_cover(book):
                
                books.append(
                    prepare_book(book)
                )


            # Stop once books match the requested count
            if len(books) >= count:


                _homepage_cache = books

                _homepage_cache_time = time.time()


                return books[:count]

    # If API fails, use old cached data
    if _homepage_cache:

        return _homepage_cache



    logger.warning(
        "Unable to load homepage carousel."
    )


    return []



# -----------------------------
# DATABASE BOOK FUNCTION
# -----------------------------


def get_or_create_book(book_id):
    """
    Finds a book in the database.

    If it does not exist:
    - gets it from Google API
    - saves it
    """

    # Check database first
    book = Book.query.filter_by(
        google_book_id=book_id
    ).first()



    if book:

        return book



    # Get book from API
    api_book = get_book_details(
        book_id
    )



    if not api_book:

        return None



    volume_info = api_book.get(
        "volumeInfo",
        {}
    )



    # Create database object
    book = Book(

        google_book_id=book_id,

        title=volume_info.get(
            "title",
            "Unknown Title"
        ),

        authors=", ".join(
            volume_info.get(
                "authors",
                []
            )
        ),

        cover_image=volume_info.get(
            "displayCover",
            ""
        )

    )



    db.session.add(book)



    try:

        db.session.commit()



    except IntegrityError:

        # Another request may have created it already
        db.session.rollback()


        book = Book.query.filter_by(
            google_book_id=book_id
        ).first()



    return book