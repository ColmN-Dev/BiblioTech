import os 

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql:///default.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
