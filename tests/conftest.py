# tests/conftest.py

import pytest
from app import create_app, db, bcrypt
from app.models import User
from app.config import Config
import os

# Custom configuration class for testing while using environment variables for sensitive information like database credentials
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql://postgres:505505@localhost:5432/bibliotech_test"
    )

# Fixture to create a test application context for database setup and removal 
@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        print(db.metadata.tables.keys())
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

# Fixture to create a test client for the Flask application
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

# Fixture to create a test client with an authenticated user
@pytest.fixture
def auth_client(app):
    
    # Set up the application context that allows database operations and session management
    with app.test_client() as client:
        with app.app_context():

            # Create a test user with a hashed password
            user = User(
                username="testuser",
                # Match the password requirements of the application (e.g., minimum length, special characters)
                password_hash=bcrypt.generate_password_hash("Password123!").decode("utf-8")
            )

            # Add the user to the database and commit the changes
            db.session.add(user)
            db.session.commit()

            # Use the session_transaction context manager to set the user ID in the session to simulate a logged-in user
            with client.session_transaction() as session:
                session["_user_id"] = str(user.id)

            yield client