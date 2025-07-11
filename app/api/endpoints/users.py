from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.schemas.response import ResponseModel
from app.services import user_service
from app.database import get_db
from app.core.deps import get_current_active_user, get_admin_user, get_manager_or_admin_user

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await user_service.create_user(db, user_in)
    return user


@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    # Prevent users from changing their own role
    if user_in.role is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Changing your own role is not allowed"
        )
        
    user = await user_service.update_user(db, current_user, user_in)
    return user


@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await user_service.get_user_by_id(db, user_id=user_id)
    return user


@router.delete("/{user_id}", response_model=ResponseModel[UserSchema])
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_manager_or_admin_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a user.
    
    - Requires manager or admin role
    - Admins can delete any user
    - Managers can delete regular users but not admins
    - Users cannot delete themselves
    """
    deleted_user = await user_service.delete_user(db, user_id, current_user)
    return ResponseModel(
        success=True, 
        message=f"User with ID {user_id} successfully deleted",
        data=deleted_user
    )


@router.patch("/{user_id}/role", response_model=UserSchema)
async def update_user_role(
    user_id: int,
    *,
    role: UserRole = Body(..., embed=True),
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a user's role.
    
    - Requires admin role
    - Admins can change anyone's role except their own
    """
    user = await user_service.update_user_role(db, user_id, role, current_user)
    return user
