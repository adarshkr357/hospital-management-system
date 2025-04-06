from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
import secrets
from typing import Any
from pydantic import BaseModel

from ....core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
)
from ....utils.db_utils import execute_query
from ....utils.validators import validate_email, validate_password_strength
from ....utils.email_utils import send_email
from ....sql.queries.auth_queries import (
    CREATE_USER_QUERY,
    GET_USER_BY_EMAIL_QUERY,
    UPDATE_PASSWORD_QUERY,
    CREATE_PASSWORD_RESET_TOKEN_QUERY,
    VERIFY_RESET_TOKEN_QUERY,
    INVALIDATE_RESET_TOKEN_QUERY,
)
from ....config.settings import settings

router = APIRouter()

class UserRegister(BaseModel):
    email: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

@router.post("/register")
async def register(user_data: UserRegister):
    if not validate_email(user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    valid, message = validate_password_strength(user_data.password)
    if not valid:
        raise HTTPException(status_code=400, detail=message)
    
    existing_user = execute_query(
        GET_USER_BY_EMAIL_QUERY, (user_data.email,), fetch_one=True
    )
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_data.password)
    
    try:
        user_id = execute_query(
            CREATE_USER_QUERY,
            (user_data.email, hashed_password, user_data.role),
            fetch_one=True,
        )["id"]
        
        # Generate an access token
        access_token = create_access_token(
            data={"sub": str(user_id), "email": user_data.email, "role": user_data.role}
        )
        # Optionally, send a welcome email:
        # await send_email(
        #     to_email=user_data.email,
        #     subject="Welcome to Hospital Management System",
        #     body_text="Thank you for registering with our system.",
        # )
        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "user_role": user_data.role
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user_data: UserLogin):
    user = execute_query(
        GET_USER_BY_EMAIL_QUERY, (user_data.email,), fetch_one=True
    )
    
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user_data.email, "role": user["role"]}
    )
    
    return {
        "message": "User logged in successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user_role": user["role"],
    }

@router.post("/forgot-password")
async def forgot_password(email: str):
    user = execute_query(GET_USER_BY_EMAIL_QUERY, (email,), fetch_one=True)
    
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    reset_token = secrets.token_urlsafe(32)
    
    execute_query(CREATE_PASSWORD_RESET_TOKEN_QUERY, (user["id"], reset_token))
    
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    
    # Optionally, send reset email:
    # await send_email(
    #     to_email=email,
    #     subject="Password Reset Request",
    #     body_text=f"""
    #     You have requested to reset your password.
    #     Please click the following link to reset your password:
    #     {reset_link}
    #
    #     This link will expire in 1 hour.
    #     If you didn't request this, please ignore this email.
    #     """,
    # )
    
    return {"message": "Password reset instructions sent to your email"}

@router.post("/reset-password")
async def reset_password(payload: PasswordReset):
    result = execute_query(VERIFY_RESET_TOKEN_QUERY, (payload.token,), fetch_one=True)
    
    if not result:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    valid, message = validate_password_strength(payload.new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=message)
    
    hashed_password = get_password_hash(payload.new_password)
    user_id = result["user_id"]
    
    execute_query(UPDATE_PASSWORD_QUERY, (hashed_password, user_id))
    execute_query(INVALIDATE_RESET_TOKEN_QUERY, (payload.token,))
    
    return {"message": "Password reset successful"}

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    # Returning only the role under our new naming convention.
    return {"access_token": None, "user_role": current_user["role"]}

@router.post("/change-password")
async def change_password(
    old_password: str, new_password: str, current_user: dict = Depends(get_current_user)
):
    if not verify_password(old_password, current_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    valid, message = validate_password_strength(new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=message)
    
    hashed_password = get_password_hash(new_password)
    
    execute_query(UPDATE_PASSWORD_QUERY, (hashed_password, current_user["email"]))
    
    return {"message": "Password changed successfully"}
