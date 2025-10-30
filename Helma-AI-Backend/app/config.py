import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file if it exists
load_dotenv()

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your-refresh-secret-key-for-jwt")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Settings class for easier access to configuration
class Settings(BaseSettings):
    JWT_SECRET_KEY: str = SECRET_KEY
    JWT_REFRESH_SECRET_KEY: str = REFRESH_SECRET_KEY
    JWT_ALGORITHM: str = ALGORITHM
    MONGODB_URI: str = MONGODB_URI
    DB_NAME: str = DB_NAME
    ACCESS_TOKEN_EXPIRE_MINUTES: int = ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAYS: int = REFRESH_TOKEN_EXPIRE_DAYS

settings = Settings() 