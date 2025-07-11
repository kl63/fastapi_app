from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """
    Standard response model for API endpoints
    """
    success: bool
    message: str
    data: Optional[T] = None
    

class PaginatedResponseModel(ResponseModel[List[T]]):
    """
    Response model for paginated results
    """
    total: int
    page: int
    size: int
    pages: int
