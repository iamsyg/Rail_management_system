from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseSettings
from datetime import timedelta
import os
from dotenv import load_dotenv
import uvicorn
import gc
import threading
import time
import atexit

# Load environment variables first
load_dotenv()

# Set memory optimization environment variables
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['PYTHONHASHSEED'] = '0'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

# Import routers after setting environment variables
from .auth import auth_router
from .complaint import complaint_router 

# Import database connection
from database.lib.prisma import prisma

class Settings(BaseSettings):
    authjwt_secret_key: str = os.environ.get("FLASK_JWT_SECRET_KEY", "default-key")
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

# Memory management functions
def cleanup_all_models():
    """Clean up all ML models to free memory"""
    try:
        # Import cleanup functions when needed to avoid import errors
        from utils.ml_pipeline import cleanup_models as cleanup_ml_models
        from utils.classifier import cleanup_models as cleanup_classifier_models
        
        cleanup_ml_models()
        cleanup_classifier_models()
        gc.collect()
        print("All models cleaned up successfully")
    except ImportError as e:
        print(f"Could not import cleanup functions: {e}")
    except Exception as e:
        print(f"Error during model cleanup: {e}")

def periodic_cleanup():
    """Periodic memory cleanup"""
    while True:
        try:
            time.sleep(300)  # Every 5 minutes
            gc.collect()
            print("Periodic memory cleanup performed")
            
            # Aggressive cleanup every 30 minutes
            if int(time.time()) % 1800 == 0:
                cleanup_all_models()
                print("Aggressive model cleanup performed")
                
        except Exception as e:
            print(f"Error during periodic cleanup: {e}")

# Start cleanup thread
cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
cleanup_thread.start()

# Register cleanup on exit
atexit.register(cleanup_all_models)

def create_app():
    # Create FastAPI app with memory optimizations
    app = FastAPI(
        title="Complaint Classification API",
        description="API for classifying user complaints",
        version="1.0.0",
        docs_url="/docs" if os.environ.get("ENVIRONMENT") != "production" else None,
        redoc_url="/redoc" if os.environ.get("ENVIRONMENT") != "production" else None
    )
    
    # Setup CORS with more restrictive settings for production
    frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
    allowed_origins = [frontend_url]
    
    # Add common domains for development
    if os.environ.get("ENVIRONMENT") != "production":
        allowed_origins.extend([
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://localhost:3000"
        ])
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type", 
            "Authorization", 
            "X-Requested-With", 
            "X-CSRF-TOKEN", 
            "x-csrf-token"
        ],
        max_age=3600,  # Cache preflight requests
    )
    
    # JWT Configuration
    @AuthJWT.load_config
    def get_config():
        return Settings()
    
    # Exception handler for AuthJWT
    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        error_responses = {
            "Token has expired": {
                "status_code": 401,
                "content": {"message": "Token has expired", "error": "token_expired"}
            },
            "Signature verification failed": {
                "status_code": 401,
                "content": {"message": "Signature verification failed", "error": "invalid_token"}
            }
        }
        
        for error_msg, response in error_responses.items():
            if error_msg in exc.message:
                return JSONResponse(**response)
        
        return JSONResponse(
            status_code=401,
            content={"message": "Request doesn't contain valid token", "error": exc.message}
        )
    
    # Global exception handler for better error handling
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        print(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "error": str(exc)}
        )
    
    # Register routers
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(complaint_router, prefix="/complaints", tags=["Complaints"])
    
    # Health check routes
    @app.get("/", tags=["Health"])
    async def root():
        return {"message": "Complaint Classification API", "status": "running"}
    
    @app.get("/status", tags=["Health"])
    async def status():
        return {"message": "Success", "status": "online"}
    
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Detailed health check"""
        try:
            # Check database connection
            db_status = "connected" if prisma.is_connected() else "disconnected"
            
            # Check memory usage
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            return {
                "status": "healthy",
                "database": db_status,
                "memory_usage_mb": f"{memory_mb:.1f}",
                "environment": os.environ.get("ENVIRONMENT", "development")
            }
        except Exception as e:
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "error": str(e)}
            )
    
    # Startup and shutdown events
    @app.on_event("startup")
    async def startup():
        print("[Server] Starting up...")
        print(f"[Environment] {os.environ.get('ENVIRONMENT', 'development')}")
        print("[Prisma] Connecting Prisma client...")
        await prisma.connect()
        print("[Server] Startup complete")
    
    @app.on_event("shutdown")
    async def shutdown():
        print("[Server] Shutting down...")
        
        # Cleanup models
        cleanup_all_models()
        
        # Disconnect database
        if prisma.is_connected():
            print("[Prisma] Disconnecting Prisma client...")
            await prisma.disconnect()
        
        print("[Server] Shutdown complete")
    
    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Get port from environment variable (Render uses PORT)
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"  # Important: bind to all interfaces for Render
    
    print(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "website.app.pages.api.user.server:app", 
        host=host, 
        port=port, 
        reload=False,  # Disable reload in production
        workers=1,     # Single worker to save memory
        access_log=False,  # Disable access logs to reduce I/O
        log_level="info"
    )