from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import time

from app.database import get_db

router = APIRouter()


@router.get("/")
async def health_check():
    """
    Basic health check endpoint that returns system status
    """
    return {
        "status": "ok",
        "timestamp": time.time(),
        "service": "fastapi-user-management",
    }


@router.get("/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """
    Database health check that verifies database connection
    """
    try:
        # Simple query to check database connectivity
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            return {
                "status": "ok",
                "database": "connected",
                "timestamp": time.time(),
            }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e),
            "timestamp": time.time(),
        }
