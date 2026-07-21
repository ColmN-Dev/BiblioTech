# tests/test_reviews.py

def test_review_requires_login(client):
    response = client.post(
        "/book/test-book/review",
        data={
            "rating": 5,
            "review_text": "Great book!"
        }
    )

    assert response.status_code == 302
    
def test_delete_review_requires_auth(client):
    response = client.post("/book/test-book/review/delete")

    assert response.status_code == 302
    
# Test invalid rating is rejected
def test_invalid_review_rating(auth_client):
    response = auth_client.post(
        "/book/test-book/review",
        data={
            "rating": 10,
            "review_text": "Test"
        },
        follow_redirects=True
    )

    assert response.status_code == 200