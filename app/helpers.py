import requests
import random
import os

from dotenv import load_dotenv
load_dotenv()

# Set the base URL for the Google Books API
Base_URL = "https://www.googleapis.com/books/v1/volumes"

# Get the API key from environment variables
API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")  

# Google Books API needs API key passed as a query param on every request

def fetch_json(params):
    """Send request to fetch JSON data from the API."""
    try:
        params["key"] = API_KEY  # Add the API key to the parameters
        response = requests.get(Base_URL , params=params, timeout=10)
        # Raise an error for bad HTTP responses (e.g. 404, 500)
        response.raise_for_status()
        
        return response.json()
    
    # Handle JSON parsing errors and print an error message for debugging
    except ValueError:
        print("Error parsing JSON response.")
        return None
    
    # Handle any exceptions that occur during the request and print an error message
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
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
    return data.get("items") if data else []

def get_book_details(volume_id):
    """Get detailed information about a specific book using its volume ID."""
    try:
        response = requests.get(f"{Base_URL}/volumes/{volume_id}", params={"key": API_KEY}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching book {volume_id}: {e}")
        return None
    
def get_random_books(count=4):
    """Fetch a list of random books for the homepage carousel on each page refresh."""
    # Use a random search term/letter to get a variety of books
    letters = "abcdefghijklmnopqrstuvwxyz"
    query = random.choice(letters)
    start_index = random.randint(0, 300)  # Random start index for unique results
    
    data = fetch_json({
        "q": query,
        "maxResults": count,
        "startIndex": start_index
    })
    
    items = data.get("items") if data else []
    return items[:count]  # Return only the requested number of books
    
    