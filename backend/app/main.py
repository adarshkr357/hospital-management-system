import datetime
import os
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .config.database import initialize_database
from .api.v1.api import api_router

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    # Initialize database
    if not initialize_database():
        logger.error("Failed to initialize database")
        raise Exception("Database initialization failed")
    else:
        logger.info("Database initialized successfully")

    app = FastAPI(
        title=os.getenv("PROJECT_NAME"),
        debug=os.getenv("DEBUG", "False").lower() == "true",
    )

    # Configure CORS
    origins = eval(os.getenv("BACKEND_CORS_ORIGINS", "[]"))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=os.getenv("API_V1_STR", "/api/v1"))

    return app


app = create_app()


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Hospital Management System API",
        "version": "1.0",
        "status": "active",
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
    )
    logger.info("Application started")
    