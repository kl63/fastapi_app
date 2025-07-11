import asyncio
import logging
from typing import Optional

from app.database import Base, engine, get_db
from app.core.config import settings
from app.crud.user import user as user_crud
from app.schemas.user import UserCreate
from app.models.user import UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_admin(
    email: str,
    password: str,
    username: str,
    role: UserRole,
    db_session
) -> None:
    """Create an admin user if one doesn't already exist"""
    try:
        user = await user_crud.get_by_email(db=db_session, email=email)
        if user:
            logger.info(f"Admin user {email} already exists")
            return
        
        user_in = UserCreate(
            email=email,
            username=username,
            password=password,
            role=role
        )
        user = await user_crud.create(db=db_session, obj_in=user_in)
        logger.info(f"Admin user {email} created successfully")
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        raise


async def init_db() -> None:
    """Initialize database, create tables, and create users with different roles"""
    try:
        # Create tables if they don't exist
        async with engine.begin() as conn:
            logger.info("Creating tables if they don't exist...")
            # This will not recreate tables that already exist
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Tables created successfully")
        
        # Create users with different roles
        async for session in get_db():
            # Create admin user
            await create_admin(
                email="admin@example.com",
                password="adminpassword",
                username="admin",
                role=UserRole.ADMIN,
                db_session=session
            )
            
            # Create manager user
            await create_admin(
                email="manager@example.com",
                password="managerpassword",
                username="manager",
                role=UserRole.MANAGER,
                db_session=session
            )
            
            # Create regular user
            await create_admin(
                email="user@example.com",
                password="userpassword",
                username="testuser",
                role=UserRole.USER,
                db_session=session
            )
            
            break
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    logger.info("Initializing database...")
    asyncio.run(init_db())
    logger.info("Database initialization completed")
