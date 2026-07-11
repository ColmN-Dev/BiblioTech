import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")

if not API_KEY:
    raise RuntimeError("Google Books API key is missing")


# Popular book genres used to fetch random books for the homepage.
# This list can also be reused anywhere else genres are needed.
BOOK_GENRES = [
    "Fiction",
    "Fantasy",
    "Science Fiction",
    "Mystery",
    "Thriller",
    "Romance",
    "Horror",
    "Adventure",
    "Crime",
    "Biography",
    "Autobiography",
    "History",
    "Science",
    "Technology",
    "Computer Science",
    "Programming",
    "Business",
    "Economics",
    "Finance",
    "Self Help",
    "Psychology",
    "Philosophy",
    "Religion",
    "Spirituality",
    "Health",
    "Fitness",
    "Travel",
    "Cooking",
    "Food",
    "Art",
    "Photography",
    "Music",
    "Poetry",
    "Drama",
    "Classics",
    "Literature",
    "Politics",
    "Law",
    "Education",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Medicine",
    "Engineering",
    "Environment",
    "Nature",
    "Sports",
    "Children",
    "Young Adult",
    "Comics",
    "Graphic Novels"
]


def add_custom_links(book):
    """
    Adds Amazon, Goodreads and WorldCat search links
    using the book's ISBN.
    """

    if not book or "volumeInfo" not in book:
        return book

    volume_info = book["volumeInfo"]

    isbn = None

    # Google Books may return both ISBN-10 and ISBN-13.
    # ISBN-13 is preferred because it is the current standard.
    for item in volume_info.get("industryIdentifiers", []):

        if item["type"] == "ISBN_13":
            isbn = item["identifier"]
            break

        elif item["type"] == "ISBN_10":
            isbn = item["identifier"]

    volume_info["customLinks"] = {}

    if isbn:

        # Remove spaces and hyphens before creating search links.
        isbn = isbn.replace("-", "").replace(" ", "")

        volume_info["customLinks"] = {
            "amazon": f"https://www.amazon.com/s?k={isbn}",
            "goodreads": f"https://www.goodreads.com/search?q={isbn}",
            "worldcat": f"https://search.worldcat.org/search?q={isbn}"
        }

    return book


def fetch_json(params, url=BASE_URL):
    """
    Sends a request to the Google Books API and
    returns the JSON response.
    """

    try:

        # Include the API key with every request.
        params["key"] = API_KEY

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(error)
        return None


def search_books(query, max_results=20):
    """
    Searches Google Books using a title,
    author or keyword.
    """

    data = fetch_json({
        "q": query,
        "maxResults": max_results,
        "printType": "books"
    })

    if not data:
        return []

    books = data.get("items", [])

    return [
        add_custom_links(book)
        for book in books
    ]


def get_book_details(volume_id):
    """
    Retrieves detailed information
    for a single book.
    """

    data = fetch_json(
        {},
        url=f"{BASE_URL}/{volume_id}"
    )

    if data:
        return add_custom_links(data)

    return None


def get_random_books(count=5):
    """
    Selects a random genre and returns
    books for the homepage carousel.
    """

    genre = random.choice(BOOK_GENRES)

    data = fetch_json({
        "q": f"subject:{genre}",
        "maxResults": count
    })

    if not data:
        return []

    books = data.get("items", [])

    return [
        add_custom_links(book)
        for book in books[:count]
    ]
