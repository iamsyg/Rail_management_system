# from fastapi import FastAPI, Request, Depends, HTTPException, Response
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from fastapi.security import OAuth2PasswordBearer
# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# from pydantic import BaseSettings
# from datetime import timedelta
# import os
# from dotenv import load_dotenv
# import uvicorn

# # Import blueprints (converted to routers in FastAPI)
# from .auth import auth_router
# from .complaint import complaint_router 

# # Import database connection
# from database.lib.prisma import prisma

# # Load environment variables
# load_dotenv()

# class Settings(BaseSettings):
#     authjwt_secret_key: str = os.environ.get("FLASK_JWT_SECRET_KEY", "default-key")
#     authjwt_access_token_expires: timedelta = timedelta(days=2)
#     authjwt_refresh_token_expires: timedelta = timedelta(days=7)
#     authjwt_token_location: set = {"cookies", "headers"}
#     authjwt_cookie_secure: bool = os.environ.get("ENVIRONMENT") == "production"
#     authjwt_access_cookie_name: str = "access_token"
#     authjwt_refresh_cookie_name: str = "refresh_token"
#     authjwt_cookie_csrf_protect: bool = os.environ.get("ENVIRONMENT") == "production"
#     authjwt_access_cookie_path: str = "/"
#     authjwt_refresh_cookie_path: str = "/auth/refresh"
#     authjwt_cookie_samesite: str = "lax"

# def create_app():
#     app = FastAPI()
    
#     # Setup CORS
#     frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[frontend_url],
#         allow_credentials=True,
#         allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#         allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-CSRF-TOKEN", "x-csrf-token"],
#     )
    
#     # JWT Configuration
#     @AuthJWT.load_config
#     def get_config():
#         return Settings()
    
#     # Exception handler for AuthJWT
#     @app.exception_handler(AuthJWTException)
#     def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#         if exc.message == "Token has expired":
#             return JSONResponse(
#                 status_code=401,
#                 content={"message": "Token has expired", "error": "token_expired"}
#             )
#         elif "Signature verification failed" in exc.message:
#             return JSONResponse(
#                 status_code=401,
#                 content={"message": "Signature verification failed", "error": "invalid_token"}
#             )
#         else:
#             return JSONResponse(
#                 status_code=401,
#                 content={"message": "Request doesn't contain valid token", "error": exc.message}
#             )
    
#     # Register routers (equivalent to blueprints in Flask/Quart)
#     app.include_router(auth_router, prefix="/auth")
#     app.include_router(complaint_router, prefix="/complaints")
    
#     # Routes
#     @app.get("/status")
#     async def status():
#         return {"message": "Success", "status": "online"}
    
#     # Startup and shutdown events for Prisma
#     @app.on_event("startup")
#     async def startup():
#         print("[Prisma] Connecting Prisma client...")
#         await prisma.connect()
    
#     @app.on_event("shutdown")
#     async def shutdown():
#         if prisma.is_connected():
#             print("[Prisma] Disconnecting Prisma client...")
#             await prisma.disconnect()
    
#     return app

# # Create the application instance
# app = create_app()

# if __name__ == "__main__":
#     uvicorn.run("website.app.pages.api.user.server:app", host="127.0.0.1", port=8080, reload=True)









from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic_settings import BaseSettings
from datetime import timedelta
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import uvicorn

# Import blueprints (converted to routers in FastAPI)
from .auth import auth_router
from .complaint import complaint_router 

# Import database connection
from database.lib.prisma import prisma

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    authjwt_secret_key: str = os.environ.get("FLASK_JWT_SECRET_KEY", "eternity")
    authjwt_access_token_expires: timedelta = timedelta(days=2)
    authjwt_refresh_token_expires: timedelta = timedelta(days=7)
    authjwt_token_location: set = {"cookies", "headers"}
    authjwt_cookie_secure: bool = os.environ.get("ENVIRONMENT") == "production"
    authjwt_access_cookie_name: str = "access_token"
    authjwt_refresh_cookie_name: str = "refresh_token"
    authjwt_cookie_csrf_protect: bool = os.environ.get("ENVIRONMENT") == "production"
    authjwt_access_cookie_path: str = "/"
    authjwt_refresh_cookie_path: str = "/auth/refresh"
    authjwt_cookie_samesite: str = "lax"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[Prisma] Connecting Prisma client...")
    await prisma.connect()
    yield
    # Shutdown
    if prisma.is_connected():
        print("[Prisma] Disconnecting Prisma client...")
        await prisma.disconnect()

def create_app():
    app = FastAPI(lifespan=lifespan)
    
    # Setup CORS
    frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-CSRF-TOKEN", "x-csrf-token"],
    )
    
    # Exception handler for JWT errors
    @app.exception_handler(jwt.ExpiredSignatureError)
    def jwt_expired_handler(request: Request, exc: jwt.ExpiredSignatureError):
        return JSONResponse(
            status_code=401,
            content={"message": "Token has expired", "error": "token_expired"}
        )
    
    @app.exception_handler(jwt.InvalidSignatureError)
    def jwt_invalid_signature_handler(request: Request, exc: jwt.InvalidSignatureError):
        return JSONResponse(
            status_code=401,
            content={"message": "Signature verification failed", "error": "invalid_token"}
        )
    
    @app.exception_handler(jwt.InvalidTokenError)
    def jwt_invalid_token_handler(request: Request, exc: jwt.InvalidTokenError):
        return JSONResponse(
            status_code=401,
            content={"message": "Request doesn't contain valid token", "error": str(exc)}
        )
    
    # Register routers (equivalent to blueprints in Flask/Quart)
    app.include_router(auth_router, prefix="/auth")
    app.include_router(complaint_router, prefix="/complaints")
    
    # Routes
    @app.get("/status")
    async def status():
        return {"message": "Success", "status": "online"}
    
    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("website.app.pages.api.user.server:app", host="0.0.0.0", port=port, reload=False)