from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import json
import os
from app.routers import student,teacher, classroom, login, school
from app.database import ping_database

# Create FastAPI app
app = FastAPI(
    title="FastAPI Backend",
    description="FastAPI backend with MongoDB, authentication, and AI vision capabilities",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers with API versioning

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to FastAPI Backend API",
        "docs": "/docs",
        "version": "0.1.0"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status of the API and its dependencies
    """
    db_status, db_error = await ping_database()
    
    health_data = {
        "status": "healthy" if db_status else "unhealthy",
        "database": {
            "connected": db_status,
            "error": db_error
        },
        "version": app.version
    }
    
    return health_data





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 