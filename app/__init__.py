from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Initialize SQLAlchemy instance for database management
db = SQLAlchemy()

# Load configuration from config object
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Register the routes blueprint
    from .routes import routes
    app.register_blueprint(routes)
    
    return app