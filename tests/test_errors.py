def test_404_error(client):
    # Simulate a request to a non-existent route to trigger a 404 error
    response = client.get('/this-page-does-not-exist')
    
    # Assert that the response status code is 404
    assert response.status_code == 404