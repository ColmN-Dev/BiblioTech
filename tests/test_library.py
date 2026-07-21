# tests/test_library.py

def test_library_requires_login(client):
    response = client.get("/library")

    assert response.status_code == 302
    
# Test the library page with an authenticated client
def test_library_page(auth_client):
    response = auth_client.get("/library")

    assert response.status_code == 200
    
# Test library redirects if user is not logged in
def test_library_requires_login(client):
    response = client.get("/library")

    assert response.status_code == 302
    
# Test adding a book redirects successfully
def test_add_book(auth_client):
    response = auth_client.post("/library/add/test-book")

    assert response.status_code == 302
    
# Test removing a book redirects successfully
def test_remove_book(auth_client):
    response = auth_client.post("/library/remove/test-book")

    assert response.status_code == 302