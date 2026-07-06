from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Initialize SQLAlchemy and Migrate instances for database management
db = SQLAlchemy()
migrate = Migrate()

# Load configuration from config object
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize the database and migration tool with the app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to register them with SQLAlchemy
    from .models import User, User_Library, Book, Review 
    
    # Register the routes blueprint
    from .routes import routes
    app.register_blueprint(routes)
    
    return app