import os
from dotenv import load_dotenv

load_dotenv()

# Configuration class for the Flask application. It sets up the secret key and database URI, using environment variables if available, or default values otherwise.
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Disable SQLAlchemy event system to save resources, as it is not needed for this application.
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
