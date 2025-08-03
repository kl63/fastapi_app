import asyncio
import logging
from typing import Optional

from app.database import Base, engine, get_db
from app.core.config import settings
from app.crud.user import general_user as general_user_crud, freshcart_user as freshcart_user_crud
from app.schemas.user import UserCreate
from app.models.user import UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_admin(
    email: str,
    password: str,
    username: str,
    role: UserRole,
    db_session,
    is_freshcart: bool = False
) -> None:
    """Create an admin user if one doesn't already exist"""
    try:
        # Choose the appropriate CRUD based on frontend
        crud = freshcart_user_crud if is_freshcart else general_user_crud
        
        user = await crud.get_by_email(db=db_session, email=email)
        if user:
            logger.info(f"Admin user {email} already exists for {'FreshCart' if is_freshcart else 'General API'}")
            return
        
        user_in = UserCreate(
            email=email,
            username=username,
            password=password,
            role=role
        )
        user = await crud.create(db=db_session, obj_in=user_in)
        logger.info(f"Admin user {email} created successfully for {'FreshCart' if is_freshcart else 'General API'}")
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        raise


async def init_db() -> None:
    """Initialize database, create tables, and create users with different roles for both frontends"""
    try:
        # Create tables if they don't exist
        async with engine.begin() as conn:
            logger.info("Creating tables if they don't exist...")
            # This will not recreate tables that already exist
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Tables created successfully")
        
        # Create users with different roles for both frontends
        async for session in get_db():
            # Create users for General API (users_general table)
            logger.info("Creating users for General API...")
            
            # Create admin user for General API
            await create_admin(
                email="admin@example.com",
                password="adminpassword",
                username="admin",
                role=UserRole.ADMIN,
                db_session=session,
                is_freshcart=False
            )
            
            # Create manager user for General API
            await create_admin(
                email="manager@example.com",
                password="managerpassword",
                username="manager",
                role=UserRole.MANAGER,
                db_session=session,
                is_freshcart=False
            )
            
            # Create regular user for General API
            await create_admin(
                email="user@example.com",
                password="userpassword",
                username="testuser",
                role=UserRole.USER,
                db_session=session,
                is_freshcart=False
            )
            
            # Create users for FreshCart frontend (users_freshcart table)
            logger.info("Creating users for FreshCart frontend...")
            
            # Create admin user for FreshCart
            await create_admin(
                email="fcadmin@example.com",
                password="adminpassword",
                username="fcadmin",
                role=UserRole.ADMIN,
                db_session=session,
                is_freshcart=True
            )
            
            # Create manager user for FreshCart
            await create_admin(
                email="fcmanager@example.com",
                password="managerpassword",
                username="fcmanager",
                role=UserRole.MANAGER,
                db_session=session,
                is_freshcart=True
            )
            
            # Create regular user for FreshCart
            await create_admin(
                email="fcuser@example.com",
                password="userpassword",
                username="fctestuser",
                role=UserRole.USER,
                db_session=session,
                is_freshcart=True
            )
            
            break
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    logger.info("Initializing database...")
    asyncio.run(init_db())
    logger.info("Database initialization completed")
