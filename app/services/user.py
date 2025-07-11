from typing import List, Optional, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user as user_crud
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        user = await user_crud.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    async def get_users(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return await user_crud.get_multi(db, skip=skip, limit=limit)

    @staticmethod
    async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
        # Check if email is already registered
        existing_user = await user_crud.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username is already registered
        existing_username = await user_crud.get_by_username(db, username=user_in.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        return await user_crud.create(db, obj_in=user_in)

    @staticmethod
    async def update_user(
        db: AsyncSession, current_user: User, user_in: UserUpdate
    ) -> User:
        # Check if email update is requested and if it's available
        if user_in.email and user_in.email != current_user.email:
            existing_user = await user_crud.get_by_email(db, email=user_in.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Check if username update is requested and if it's available
        if user_in.username and user_in.username != current_user.username:
            existing_user = await user_crud.get_by_username(db, username=user_in.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
        
        return await user_crud.update(db, db_obj=current_user, obj_in=user_in)


user_service = UserService()
