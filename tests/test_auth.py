# Run authentication-related tests
def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_signup_page(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200
    
def test_login_with_invalid_credentials(client):
    # Simulate a login attempt with invalid credentials
    response = client.post('/auth/login', data={'username': 'invalid_user', 'password': 'wrong_password'}, follow_redirects=True)
    # Assert that the response indicates a failed login
    assert response.status_code == 200  # Adjust the expected status code
    assert b'Invalid' in response.data  # Check for an error message in the response
    
def test_logout(client):
    # Simulate a logout request
    response = client.get('/auth/logout', follow_redirects=True)
    # Assert that the response indicates a successful logout
    assert response.status_code == 200  # Adjust the expected status code for redirect to home page