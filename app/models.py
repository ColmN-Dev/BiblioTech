import datetime
from . import db 
from flask_login import UserMixin

# Define the User model with fields for id, username, password hash, and date created
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    # Define relationships to the User_Library and Review models
    library = db.relationship('User_Library', back_populates='user', cascade='all, delete-orphan', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)

# Define the User_Library model with fields for user_id, book_id, and date created
class User_Library(db.Model):
    __tablename__ = 'user_library'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    google_book_id = db.Column(db.String(120), db.ForeignKey('books.google_book_id'), primary_key=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    # Define relationships to the User and Book models
    user = db.relationship('User', back_populates='library', lazy=True)
    book = db.relationship('Book', back_populates='user_library', lazy=True)

# Define the Book model with fields for google_book_id, title, authors, cover_image, buy_links and date created
class Book(db.Model):
    __tablename__ = 'books'
    google_book_id = db.Column(db.String(120), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.Text)
    cover_image = db.Column(db.Text)
    buy_links = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    # Define relationships to the User_Library and Review models
    reviews = db.relationship('Review', back_populates='book', lazy=True)
    user_library = db.relationship('User_Library', back_populates='book', lazy=True)
    
# Define the Review model with fields for review_id, user_id, book_id, rating, review_text and date created
class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Make user_id nullable to allow for anonymous reviews
    google_book_id = db.Column(db.String(120), db.ForeignKey('books.google_book_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    # Ensure that a user can only submit one review per book by adding a unique constraint on the combination of user_id and google_book_id
    __table_args__ = (
        db.UniqueConstraint('user_id', 'google_book_id', name='unique_user_book_review'),
    )
    
    # Define relationships to the User and Book models
    user = db.relationship('User', back_populates='reviews', lazy=True)
    book = db.relationship('Book', back_populates='reviews', lazy=True)
    