# from fastapi import APIRouter, Request, Depends, HTTPException, Response
# from fastapi.responses import JSONResponse
# from fastapi_jwt_auth import AuthJWT
# from pydantic import BaseModel
# from database.lib.prisma import get_prisma_client
# from uuid import uuid4
# from werkzeug.security import generate_password_hash, check_password_hash
# import enum
# from datetime import datetime
# from typing import Optional, Dict, Any, Tuple, Union

# # Define auth router
# auth_router = APIRouter()

# # Pydantic models for request validation
# class UserSignup(BaseModel):
#     name: str
#     email: str
#     phoneNumber: str
#     password: str

# class UserSignin(BaseModel):
#     email: str
#     password: str

# async def generate_access_token_and_refresh_token(user_id: str) -> Tuple[Optional[Dict[str, str]], Optional[Dict[str, Any]], int]:
#     try:
#         prisma = await get_prisma_client()
#         user = await prisma.user.find_unique(where={"id": user_id})

#         if not user:
#             return None, {
#                 "success": False,
#                 "message": "User not found"
#             }, 404

#         # Create tokens with AuthJWT
#         auth_jwt = AuthJWT()
        
#         identity = {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "phone_number": user.phoneNumber,
#             "role": user.role
#         }
        
#         access_token = auth_jwt.create_access_token(subject=user.id, user_claims=identity)
#         refresh_token = auth_jwt.create_refresh_token(subject=user.id, user_claims=identity)

#         # Save refresh token in DB
#         await prisma.user.update(
#             where={"id": user.id},
#             data={"refreshToken": refresh_token}
#         )

#         return {
#             "access_token": access_token,
#             "refresh_token": refresh_token
#         }, None, 200

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return None, {
#             "success": False,
#             "message": f"Error generating tokens: {str(e)}"
#         }, 500

# @auth_router.post("/signup", status_code=201)
# async def signup_user(user: UserSignup):
#     try:
#         name = user.name.strip()
#         email = user.email.strip().lower()
#         phone_number = user.phoneNumber.strip()
#         password = user.password.strip()

#         if not all([name, email, phone_number, password]):
#             raise HTTPException(status_code=400, detail="All fields are required")

#         prisma = await get_prisma_client()

#         existing_user = await prisma.user.find_unique(where={"email": email})
#         if existing_user:
#             raise HTTPException(status_code=409, detail="User already exists")

#         hashed_password = generate_password_hash(password)

#         new_user = await prisma.user.create(data={
#             "name": name,
#             "email": email,
#             "phoneNumber": phone_number,
#             "password": hashed_password,
#             "role": "user"
#         })

#         return {
#             "success": True,
#             "user": {
#                 "id": new_user.id,
#                 "email": new_user.email,
#                 "name": new_user.name,
#                 "phoneNumber": new_user.phoneNumber,
#                 "role": new_user.role
#             }
#         }

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# @auth_router.post("/signin")
# async def signin_user(user: UserSignin, Authorize: AuthJWT = Depends()):
#     try:
#         email = user.email.strip().lower()
#         password = user.password

#         if not email or not password:
#             raise HTTPException(status_code=400, detail="Missing email or password")

#         prisma = await get_prisma_client()
#         user_db = await prisma.user.find_unique(where={"email": email})

#         if not user_db:
#             raise HTTPException(status_code=401, detail="User not found")

#         if not check_password_hash(user_db.password, password):
#             raise HTTPException(status_code=401, detail="Invalid email or password")

#         tokens, error_response, status = await generate_access_token_and_refresh_token(user_db.id)

#         if error_response:
#             raise HTTPException(status_code=status, detail=error_response["message"])

#         access_token = tokens["access_token"]
#         refresh_token = tokens["refresh_token"]

#         response = {
#             "message": "Login successful",
#             "success": True,
#             "user": {
#                 "id": user_db.id,
#                 "name": user_db.name,
#                 "email": user_db.email,
#                 "phoneNumber": user_db.phoneNumber,
#                 "role": user_db.role
#             },
#             "access_token": access_token,
#             "refresh_token": refresh_token
#         }

#         # Set cookies
#         response_obj = JSONResponse(content=response)
#         Authorize.set_access_cookies(access_token, response_obj)
#         Authorize.set_refresh_cookies(refresh_token, response_obj)

#         return response_obj

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

# @auth_router.post("/logout")
# async def logout_user(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         user_id = Authorize.get_jwt_subject()
        
#         prisma = await get_prisma_client()
#         await prisma.user.update(where={"id": user_id}, data={"refreshToken": None})
        
#         response = JSONResponse(content={"message": "Logged out successfully"})
#         Authorize.unset_jwt_cookies(response)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @auth_router.get("/profile")
# async def get_logged_in_user(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
        
#         # Get the identity (user ID)
#         user_id = Authorize.get_jwt_subject()
        
#         # Get additional claims
#         claims = Authorize.get_raw_jwt()
        
#         return {
#             "success": True,
#             "user": {
#                 "id": user_id,
#                 "name": claims.get("name"),
#                 "email": claims.get("email"),
#                 "phone_number": claims.get("phone_number"),
#                 "role": claims.get("role")
#             }
#         }
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=str(e))

# @auth_router.post("/refresh")
# async def refresh(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_refresh_token_required()
        
#         current_user = Authorize.get_jwt_subject()
#         user_claims = Authorize.get_raw_jwt()
        
#         new_access_token = Authorize.create_access_token(subject=current_user, user_claims=user_claims)
        
#         response = JSONResponse(content={"access_token": new_access_token})
#         Authorize.set_access_cookies(new_access_token, response)
        
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=str(e))

# @auth_router.get("/debug-cookies")
# async def debug_cookies(request: Request):
#     cookies = request.cookies
#     return {
#         "success": True,
#         "cookies": {
#             "access_token_exists": "access_token" in cookies,
#             "refresh_token_exists": "refresh_token" in cookies
#         }
#     }

# @auth_router.get("/verify-token")
# async def verify_token(request: Request, Authorize: AuthJWT = Depends()):
#     try:
#         # Get token from cookie
#         token = request.cookies.get("access_token")
#         if not token:
#             raise HTTPException(status_code=401, detail="No token in cookies")
            
#         # Verify and decode token
#         Authorize.jwt_required("cookies")
#         decoded = Authorize.get_raw_jwt()
        
#         return {
#             "success": True, 
#             "decoded": decoded,
#             "sub": decoded.get("sub")
#         }
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=str(e))










from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
import jwt
from pydantic import BaseModel
from database.lib.prisma import get_prisma_client
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple, Union
import os

# Define auth router
auth_router = APIRouter()

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "eternity")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Pydantic models for request validation
class UserSignup(BaseModel):
    name: str
    email: str
    phoneNumber: str
    password: str

class UserSignin(BaseModel):
    email: str
    password: str

class AuthJWT:
    def __init__(self):
        pass
    
    def create_access_token(self, subject: str, user_claims: dict = None):
        payload = {"sub": subject, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
        if user_claims:
            payload.update(user_claims)

        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return token
    
    def create_refresh_token(self, subject: str, user_claims: dict = None):
        payload = {"sub": subject, "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)}
        if user_claims:
            payload.update(user_claims)
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return token
    
    def jwt_required(self, locations=None):
        if hasattr(self, '_current_request'):
            token = self._get_token_from_request(self._current_request)
            try:
                self._current_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
    
    def jwt_refresh_token_required(self):
        if hasattr(self, '_current_request'):
            token = self._current_request.cookies.get("refresh_token")
            if not token:
                raise HTTPException(status_code=401, detail="Refresh token required")
            try:
                self._current_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Refresh token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    def get_jwt_subject(self):
        if hasattr(self, '_current_payload'):
            return self._current_payload.get("sub")
        return None
    
    def get_raw_jwt(self):
        if hasattr(self, '_current_payload'):
            return self._current_payload
        return {}
    
    def set_access_cookies(self, access_token: str, response: JSONResponse):
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite="lax"
        )
    
    def set_refresh_cookies(self, refresh_token: str, response: JSONResponse):
        response.set_cookie(
            key="refresh_token", 
            value=refresh_token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite="lax"
        )
    
    def unset_jwt_cookies(self, response: JSONResponse):
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
    
    def _get_token_from_request(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        if not token:
            raise HTTPException(status_code=401, detail="Token required")
        return token

def get_auth_jwt(request: Request):
    auth_jwt = AuthJWT()
    auth_jwt._current_request = request
    return auth_jwt

async def generate_access_token_and_refresh_token(user_id: str) -> Tuple[Optional[Dict[str, str]], Optional[Dict[str, Any]], int]:
    try:
        prisma = await get_prisma_client()
        user = await prisma.user.find_unique(where={"id": user_id})

        if not user:
            return None, {
                "success": False,
                "message": "User not found"
            }, 404

        # Create tokens with AuthJWT
        auth_jwt = AuthJWT()
        
        identity = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phoneNumber,
            "role": user.role
        }
        
        access_token = auth_jwt.create_access_token(subject=user.id, user_claims=identity)
        refresh_token = auth_jwt.create_refresh_token(subject=user.id, user_claims=identity)

        # Save refresh token in DB
        await prisma.user.update(
            where={"id": user.id},
            data={"refreshToken": refresh_token}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, None, 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return None, {
            "success": False,
            "message": f"Error generating tokens: {str(e)}"
        }, 500

@auth_router.post("/signup", status_code=201)
async def signup_user(user: UserSignup):
    try:
        name = user.name.strip()
        email = user.email.strip().lower()
        phone_number = user.phoneNumber.strip()
        password = user.password.strip()

        if not all([name, email, phone_number, password]):
            raise HTTPException(status_code=400, detail="All fields are required")

        prisma = await get_prisma_client()

        existing_user = await prisma.user.find_unique(where={"email": email})
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists")

        hashed_password = generate_password_hash(password)

        new_user = await prisma.user.create(data={
            "name": name,
            "email": email,
            "phoneNumber": phone_number,
            "password": hashed_password,
            "role": "user"
        })

        return {
            "success": True,
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "name": new_user.name,
                "phoneNumber": new_user.phoneNumber,
                "role": new_user.role
            }
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@auth_router.post("/signin")
async def signin_user(user: UserSignin, Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        email = user.email.strip().lower()
        password = user.password

        if not email or not password:
            raise HTTPException(status_code=400, detail="Missing email or password")

        prisma = await get_prisma_client()
        user_db = await prisma.user.find_unique(where={"email": email})

        if not user_db:
            raise HTTPException(status_code=401, detail="User not found")

        if not check_password_hash(user_db.password, password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        tokens, error_response, status = await generate_access_token_and_refresh_token(user_db.id)

        if error_response:
            raise HTTPException(status_code=status, detail=error_response["message"])

        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        response = {
            "message": "Login successful",
            "success": True,
            "user": {
                "id": user_db.id,
                "name": user_db.name,
                "email": user_db.email,
                "phoneNumber": user_db.phoneNumber,
                "role": user_db.role
            },
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        # Set cookies
        response_obj = JSONResponse(content=response)
        Authorize.set_access_cookies(access_token, response_obj)
        Authorize.set_refresh_cookies(refresh_token, response_obj)

        return response_obj

    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@auth_router.post("/logout")
async def logout_user(Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        
        prisma = await get_prisma_client()
        await prisma.user.update(where={"id": user_id}, data={"refreshToken": None})
        
        response = JSONResponse(content={"message": "Logged out successfully"})
        Authorize.unset_jwt_cookies(response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.get("/profile")
async def get_logged_in_user(Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        Authorize.jwt_required()
        
        # Get the identity (user ID)
        user_id = Authorize.get_jwt_subject()
        
        # Get additional claims
        claims = Authorize.get_raw_jwt()
        
        return {
            "success": True,
            "user": {
                "id": user_id,
                "name": claims.get("name"),
                "email": claims.get("email"),
                "phone_number": claims.get("phone_number"),
                "role": claims.get("role")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        Authorize.jwt_refresh_token_required()
        
        current_user = Authorize.get_jwt_subject()
        user_claims = Authorize.get_raw_jwt()
        
        new_access_token = Authorize.create_access_token(subject=current_user, user_claims=user_claims)
        
        response = JSONResponse(content={"access_token": new_access_token})
        Authorize.set_access_cookies(new_access_token, response)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.get("/debug-cookies")
async def debug_cookies(request: Request):
    cookies = request.cookies
    return {
        "success": True,
        "cookies": {
            "access_token_exists": "access_token" in cookies,
            "refresh_token_exists": "refresh_token" in cookies
        }
    }

@auth_router.get("/verify-token")
async def verify_token(request: Request, Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        # Get token from cookie
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="No token in cookies")
            
        # Verify and decode token
        Authorize.jwt_required("cookies")
        decoded = Authorize.get_raw_jwt()
        
        return {
            "success": True, 
            "decoded": decoded,
            "sub": decoded.get("sub")
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))