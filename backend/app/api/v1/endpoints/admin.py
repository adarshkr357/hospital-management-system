from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from datetime import datetime
from ....core.security import get_current_user
from ....utils.db_utils import execute_query

GET_ALL_USERS_QUERY = """
    SELECT id, email, role, created_at
    FROM users
    ORDER BY id;
"""

GET_USER_BY_ID_QUERY = """
    SELECT id, email, role, created_at
    FROM users
    WHERE id = %s;
"""

class UserOut(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

router = APIRouter()

@router.get("/users", response_model=List[UserOut])
def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this endpoint"
        )
    users = execute_query(GET_ALL_USERS_QUERY, fetch_all=True)
    return users

@router.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this endpoint"
        )
    user = execute_query(GET_USER_BY_ID_QUERY, (user_id,), fetch_one=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
