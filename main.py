import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from loguru import logger

from app.api.api import api_router
from app.core.config import settings
from app.core.middleware.error_handler import ErrorHandlerMiddleware, validation_exception_handler
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Setup logging when application starts
    setup_logging()
    logger.info("Application starting up...")
    
    # Perform startup activities
    logger.info("Startup complete")
    
    yield  # Application runs here
    
    # Perform cleanup when application is shutting down
    logger.info("Application shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    description="FastAPI User Management System with PostgreSQL and JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom error handling middleware
app.add_middleware(ErrorHandlerMiddleware)

# Add exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint for the API"""
    return {
        "message": "Welcome to the FastAPI User Management System",
        "documentation": "/docs",
        "version": "1.0.0"
    }

