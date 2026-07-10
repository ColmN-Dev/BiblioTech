import requests
import random
import os

from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")  
if not API_KEY:
    raise RuntimeError("Google Books API key not found. Please set the 'GOOGLE_BOOKS_API_KEY' environment variable.")

# Google Books API needs API key passed as a query param on every request

def fetch_json(params, retries=2, url=BASE_URL):
    """Send request to fetch JSON data from the API."""
    
    # Retry mechanism for temporary network or API failures
    for attempt in range(retries + 1):
        try:
            request_params = { **params, "key": API_KEY }
            response = requests.get(url, params=request_params, timeout=10)
            
            # Raise an error for bad HTTP responses (e.g. 404, 500)
            response.raise_for_status()
            return response.json()
    
    # Handle any exceptions that occur during the request and print an error message
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
        "printType": "books" # Restrict results to books only
    })
    
    if not data:
        return None  # Return None if the API request failed
    
    return data.get("items", [])

def get_book_details(volume_id):
    """Get detailed information about a specific book using its volume ID."""
    
    return fetch_json(
        {},
        url=f"{BASE_URL}/{volume_id}"
    )
    
def get_random_books(count=4):
    """Fetch a list of random books for the homepage carousel on each page refresh."""
   
    letters = "abcdefghijklmnopqrstuvwxyz"
    query = random.choice(letters)
    start_index = random.randint(0, 300)  # Random start index for unique results
    
    data = fetch_json({
        "q": query,
        "maxResults": count,
        "startIndex": start_index
    })
    
    # Return only the requested number of books, or an empty list if no items are found
    items = data.get("items", []) if data else []
    return items[:count]  # Return only the requested number of books
    
    