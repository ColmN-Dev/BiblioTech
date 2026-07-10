import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")  
if not API_KEY:
    raise RuntimeError("Google Books API key not found. Please set the 'GOOGLE_BOOKS_API_KEY' environment variable.")

def _add_custom_store_links(book_item):
    """Helper to inject third-party marketplace links using the book's ISBN."""
    if not book_item or "volumeInfo" not in book_item:
        return book_item

    volume_info = book_item["volumeInfo"]
    identifiers = volume_info.get("industryIdentifiers", [])
    
    # Try to find ISBN_13 first, fall back to ISBN_10
    isbn = None
    for identifier in identifiers:
        if identifier.get("type") in ["ISBN_13", "ISBN_10"]:
            isbn = identifier.get("identifier")
            if identifier.get("type") == "ISBN_13":
                break  # Prefer ISBN_13

    # Initialize the custom links dictionary
    volume_info["customLinks"] = {}

    if isbn:
        # Sanitize ISBN by removing spaces or hyphens if any exist
        clean_isbn = isbn.replace("-", "").replace(" ", "")
        volume_info["customLinks"] = {
            "amazon": f"https://amazon.com{clean_isbn}",
            "goodreads": f"https://goodreads.com{clean_isbn}",
            "worldcat": f"https://worldcat.org{clean_isbn}"
        }

    return book_item

def fetch_json(params, retries=2, url=BASE_URL):
    """Send request to fetch JSON data from the API."""
    for attempt in range(retries + 1):
        try:
            request_params = { **params, "key": API_KEY }
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries:
                return None

# Search Results page 
def search_books(query, max_results=20, start_index=0, order_by="relevance"):
    """Search for books by title, author or keyword using the Google Books API."""
    data = fetch_json({
        "q": query,
        "maxResults": max_results,
        "startIndex": start_index,
        "orderBy": order_by,
        "printType": "books" 
    })
    
    if not data:
        return []
    
    items = data.get("items", [])
    return [_add_custom_store_links(item) for item in items]

def get_book_details(volume_id):
    """Get detailed information about a specific book using its volume ID."""
    data = fetch_json({}, url=f"{BASE_URL}/{volume_id}")
    return _add_custom_store_links(data) if data else None
    
def get_random_books(count=5):
    """Fetch a list of popular, random books for the homepage carousel."""
    popular_genres = [
        "fiction", "mystery", "thriller", "fantasy", "sci-fi", 
        "biography", "history", "science", "adventure", "romance",
        "philosophy", "psychology", "self-help", "business", "technology"
    ]
    
    for _ in range(3):
        query = random.choice(popular_genres)
        start_index = random.randint(0, 250) 
        
        data = fetch_json({
            "q": f"subject:{query}",
            "maxResults": count,
            "startIndex": start_index,
            "orderBy": "relevance",
            "printType": "books"
        })
        
        if data and "items" in data:
            items = data["items"][:count]
            return [_add_custom_store_links(item) for item in items]
            
    fallback_data = fetch_json({"q": "bestseller", "maxResults": count, "startIndex": 0})
    fallback_items = fallback_data.get("items", [])[:count] if fallback_data else []
    return [_add_custom_store_links(item) for item in fallback_items]
