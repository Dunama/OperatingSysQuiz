import os 
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # Use the complete DATABASE_URL from your .env with proper error handling
    db_url = os.getenv("DATABASE_URL")
    if db_url and '%40' in db_url:
        # Fix potentially double-encoded characters
        db_url = db_url.replace('%40', '@')
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Additional useful SQLAlchemy settings for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Detect disconnections
        'pool_recycle': 300,    # Recycle connections after 5 minutes
        'connect_args': {
            'connect_timeout': 10  # Connection timeout in seconds
        }
    }
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 3600 #1HR
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

    # Google OAuth2 config
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://os205quizapp.online/login/google/authorized")
    
    # For production
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv("OAUTHLIB_INSECURE_TRANSPORT", "False").lower() == "true"
    OAUTHLIB_RELAX_TOKEN_SCOPE = True