from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    users = await user.get_multi(db, skip=skip, limit=limit)
    return users


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    user_obj = await user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user_obj


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    return await user.get_by_email(db, email=email)


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    # Check if user with email already exists
    user_exists = await user.get_by_email(db, email=user_create.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    # Check if user with username already exists
    username_exists = await user.get_by_username(db, username=user_create.username)
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists"
        )
    
    return await user.create(db, obj_in=user_create)


async def update_user(db: AsyncSession, user_obj: User, user_update: UserUpdate) -> User:
    # If updating email, check if it conflicts with existing users
    if user_update.email and user_update.email != user_obj.email:
        existing_user = await user.get_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != user_obj.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )
    
    # If updating username, check if it conflicts with existing users
    if user_update.username and user_update.username != user_obj.username:
        existing_username = await user.get_by_username(db, username=user_update.username)
        if existing_username and existing_username.id != user_obj.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists"
            )
    
    return await user.update(db, db_obj=user_obj, obj_in=user_update)


async def delete_user(db: AsyncSession, user_id: int, current_user: User) -> User:
    """
    Delete a user by ID, with additional checks:
    - Admins can delete any user
    - Managers can delete regular users but not admins
    - Regular users cannot delete any user
    - Users cannot delete themselves
    """
    # Get the user to delete
    user_to_delete = await get_user_by_id(db, user_id)
    
    # Prevent self-deletion
    if user_to_delete.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Check permissions based on role
    if current_user.role == UserRole.ADMIN:
        # Admins can delete anyone
        pass
    elif current_user.role == UserRole.MANAGER:
        # Managers can delete regular users but not admins
        if user_to_delete.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Managers cannot delete admin users"
            )
    else:
        # Regular users cannot delete anyone
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to delete users"
        )
    
    # Proceed with deletion
    deleted_user = await user.delete(db, id=user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return deleted_user


async def update_user_role(db: AsyncSession, user_id: int, new_role: UserRole, current_user: User) -> User:
    """
    Update a user's role with permission checks:
    - Admins can change anyone's role
    - Users cannot change their own role
    - Only admins can create other admins
    """
    # Get the user to update
    user_to_update = await get_user_by_id(db, user_id)
    
    # Prevent self-role change
    if user_to_update.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    # Only admins can perform role changes
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can change user roles"
        )
    
    # Update the role
    return await user.update(db, db_obj=user_to_update, obj_in={"role": new_role})
