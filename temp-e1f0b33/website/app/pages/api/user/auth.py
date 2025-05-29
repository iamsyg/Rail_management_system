from fastapi import APIRouter, HTTPException, Depends, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, Tuple
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

from .models import User, RoleEnum
from .dependencies import get_db

# JWT Configuration
SECRET_KEY = os.getenv("FLASK_JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Security
security = HTTPBearer()

# Define auth router
auth_router = APIRouter()

# Pydantic models for request validation
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    phoneNumber: str
    password: str

class UserSignin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Token generation functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Tuple[Optional[TokenData], Optional[dict]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None, None
        token_data = TokenData(user_id=user_id)
        return token_data, payload
    except JWTError:
        return None, None

def generate_access_token_and_refresh_token(user: User, db: Session) -> Tuple[Optional[Dict[str, str]], Optional[Dict[str, Any]], int]:
    try:
        if not user:
            return None, {
                "success": False,
                "message": "User not found"
            }, 404

        # Create token payload
        token_data = {
            "sub": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phoneNumber,
            "role": user.role.value if hasattr(user.role, 'value') else user.role
        }
        
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        # Save refresh token in DB
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, None, 200

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return None, {
            "success": False,
            "message": f"Error generating tokens: {str(e)}"
        }, 500



@auth_router.post("/signup", status_code=201)
async def signup_user(user_data: UserSignup, db: Session = Depends(get_db)):
    try:
        name = user_data.name.strip()
        email = user_data.email.strip().lower()
        phone_number = user_data.phoneNumber.strip()
        password = user_data.password.strip()

        if not all([name, email, phone_number, password]):
            raise HTTPException(status_code=400, detail="All fields are required")

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(
            name=name,
            email=email,
            phone_number=phone_number,
            password=hashed_password,
            role=RoleEnum.user
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "success": True,
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "name": new_user.name,
                "phoneNumber": new_user.phoneNumber,
                "role": new_user.role.value
            }
        }

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@auth_router.post("/signin")
async def signin_user(user_data: UserSignin, db: Session = Depends(get_db)):
    try:
        email = user_data.email.strip().lower()
        password = user_data.password

        if not email or not password:
            raise HTTPException(status_code=400, detail="Missing email or password")

        # Find user in database
        user_db = db.query(User).filter(User.email == email).first()

        if not user_db:
            raise HTTPException(status_code=401, detail="User not found")

        if not check_password_hash(user_db.password, password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Generate tokens
        tokens, error_response, status_code = generate_access_token_and_refresh_token(user_db, db)

        if error_response:
            raise HTTPException(status_code=status_code, detail=error_response["message"])

        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        print(f"[DEBUG] access_token: {access_token}")
        print(f"[DEBUG] refresh_token: {refresh_token}")

        response_data = {
            "message": "Login successful",
            "success": True,
            "user": {
                "id": user_db.id,
                "name": user_db.name,
                "email": user_db.email,
                "phoneNumber": user_db.phoneNumber,
                "role": user_db.role.value
            },
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        # Create response and set cookies
        response = JSONResponse(content=response_data)
        
        # Set access token cookie
        response.set_cookie(
            key="access_token_cookie",
            value=access_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )
        
        # Set refresh token cookie
        response.set_cookie(
            key="refresh_token_cookie", 
            value=refresh_token,
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )

        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@auth_router.post("/logout")
async def logout_user(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("access_token_cookie")
        token_data, payload = verify_token(token)
        if not token_data:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = token_data.user_id

        # Fetch user from DB
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Clear refresh token from database
        user.refresh_token = None
        db.commit()
        
        # Create response and clear cookies
        response = JSONResponse(content={"message": "Logged out successfully"})
        response.delete_cookie(key="access_token_cookie")
        response.delete_cookie(key="refresh_token_cookie")
        
        return response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.get("/profile")
async def get_logged_in_user(request: Request):
    try:
        token = request.cookies.get("access_token_cookie")
        token_data, payload  = verify_token(token)
        current_user = payload 
        return {
            "success": True,
            "user": {
                "id": current_user.get("sub"),
                "name": current_user.get("name"),
                "email": current_user.get("email"),
                "phone_number": current_user.get("phone_number"),
                "role": current_user.get("role")    
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.post("/refresh")
async def refresh_token(request: Request, db: Session = Depends(get_db)):
    try:
        # Get refresh token from cookie
        refresh_token = request.cookies.get("refresh_token_cookie")
        
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token not found")
        
        # Verify refresh token
        token_data, payload = verify_token(refresh_token)
        if not token_data or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Get user from database
        user = db.query(User).filter(User.id == token_data.user_id).first()
        if not user or user.refresh_token != refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Generate new access token
        new_token_data = {
            "sub": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phoneNumber,
            "role": user.role.value
        }
        
        new_access_token = create_access_token(data=new_token_data)
        
        response = JSONResponse(content={"access_token": new_access_token})
        response.set_cookie(
            key="access_token_cookie",
            value=new_access_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.get("/debug-cookies")
async def debug_cookies(request: Request):
    cookies = request.cookies
    return {
        "success": True,
        "cookies": dict(cookies),
        "access_token_exists": "access_token_cookie" in cookies,
        "refresh_token_exists": "refresh_token_cookie" in cookies
    }

@auth_router.get("/verify-token")
async def verify_token_endpoint(request: Request):
    try:
        # Get token from cookie
        token = request.cookies.get("access_token_cookie")
        if not token:
            raise HTTPException(status_code=401, detail="No token in cookies")
            
        # Verify and decode token
        token_data, payload = verify_token(token)
        if not token_data:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {
            "success": True, 
            "decoded": payload,
            "sub": payload.get("sub")
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))