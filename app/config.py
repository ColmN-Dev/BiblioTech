import os
from dotenv import load_dotenv

load_dotenv()

# Convert PostgreSQL URLs to use the psycopg driver.
def get_database_uri():
    database_uri = os.getenv('DATABASE_URL')

    if database_uri and database_uri.startswith(('postgres://', 'postgresql://')):
        return database_uri.replace('postgres://', 'postgresql+psycopg://', 1).replace(
            'postgresql://', 'postgresql+psycopg://', 1
        )

    return database_uri

# Configuration class for the Flask application. It sets up the secret key and database URI, using environment variables if available, or default values otherwise.
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'default_secret_key'
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    
    # Disable SQLAlchemy event system to save resources, as it is not needed for this application.
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
