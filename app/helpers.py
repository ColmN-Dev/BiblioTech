import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")  
if not API_KEY:
    raise RuntimeError("Google Books API key not found. Please set the 'GOOGLE_BOOKS_API_KEY' environment variable.")

def fetch_json(params, retries=2, url=BASE_URL):
    """Send request to fetch JSON data from the API."""
    
    for attempt in range(retries + 1):
        try:
            request_params = { **params, "key": API_KEY }
            response = requests.get(url, params=request_params, timeout=10)
            
            # Raise an error for bad HTTP responses (e.g. 404, 500, 400)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            # If this was the last attempt, break out and return None
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
        return []  # Return empty list instead of None to prevent frontend crashes
    
    return data.get("items", [])

def get_book_details(volume_id):
    """Get detailed information about a specific book using its volume ID."""
    return fetch_json(
        {},
        url=f"{BASE_URL}/{volume_id}"
    )
    
def get_random_books(count=5):
    """Fetch a list of popular, random books for the homepage carousel."""
    # A list of broad, popular categories that guarantee high-quality results
    popular_genres = [
        "fiction", "mystery", "thriller", "fantasy", "sci-fi", 
        "biography", "history", "science", "adventure", "romance",
        "philosophy", "psychology", "self-help", "business", "technology"
    ]
    
    # Try up to 3 distinct random generations if an index returns 0 results
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
            return data["items"][:count]
            
    # Absolute emergency fallback if all random attempts completely failed
    fallback_data = fetch_json({"q": "bestseller", "maxResults": count, "startIndex": 0})
    return fallback_data.get("items", [])[:count] if fallback_data else []
