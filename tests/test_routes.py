# tests/test_routes.py

def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200


def test_about_page(client):
    response = client.get("/about")

    assert response.status_code == 200

# Test empty search results page
def test_search_without_query_redirects(client):
    response = client.get("/search-results")

    assert response.status_code == 302

# Test the autocomplete feature with a short query and returns an empty JSON list
def test_autocomplete_short_query_returns_empty_list(client):
    response = client.get("/auto-complete?q=a")

    assert response.status_code == 200
    assert response.json == []