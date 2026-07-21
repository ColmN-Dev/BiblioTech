from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import Config

# Initialize extensions for database management
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Load configuration from config object
def create_app(config_class=None):
    app = Flask(__name__)
    if config_class is None:
        config_class = Config
    app.config.from_object(config_class)

    # Initialize the extensions with the Flask app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Redirect to login page if not authenticated
    login_manager.login_message = None  # Explicitly set to None to avoid default flash message
    
    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User, db
        return db.session.get(User, int(user_id))
    
    # Register the routes blueprint
    from .routes import routes
    app.register_blueprint(routes)
    
    # Register the authentication blueprint
    from .auth import auth
    app.register_blueprint(auth)
    
    # Register error handlers
    from .errors import page_not_found, internal_server_error
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    
    return app