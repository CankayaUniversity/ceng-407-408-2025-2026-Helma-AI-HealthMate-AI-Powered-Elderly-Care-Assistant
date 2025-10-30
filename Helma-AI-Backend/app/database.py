from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]

# Define collection references

students_collection = db["students"]


async def ping_database():
    """
    Check if the database connection is working.
    
    Returns:
        bool: True if the connection is successful, False otherwise
        str: Error message if connection fails, None otherwise
    """
    try:
        await client.admin.command('ping')
        return True, None
    except Exception as e:
        error_msg = f"Database connection error: {str(e)}"
        return False, error_msg 