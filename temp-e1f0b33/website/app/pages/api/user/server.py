# # server.py
# from dotenv import load_dotenv
# load_dotenv()


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import os
# from datetime import timedelta

# from .auth import auth_router
# from .complaint import complaint_router
# from .database import Base, engine
# from .models import User, Complaint



# app = FastAPI()

# frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
# allowed_origins = [frontend_url]
    
#     # Add common domains for development
# if os.environ.get("ENVIRONMENT") != "production":
#     allowed_origins.extend([
#         "http://localhost:3000",
#         "http://127.0.0.1:3000",
#         "https://localhost:3000"
#     ])

# # CORS config
# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=allowed_origins,
#         allow_credentials=True,
#         allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#         allow_headers=[
#             "Content-Type", 
#             "Authorization", 
#             "X-Requested-With", 
#             "X-CSRF-TOKEN", 
#             "x-csrf-token"
#         ],
#         max_age=3600,  # Cache preflight requests
#     )

# # Create tables
# Base.metadata.create_all(bind=engine)

# # Include routers
# app.include_router(auth_router, prefix="/auth")
# app.include_router(complaint_router, prefix="/complaints")

# @app.get("/status")
# async def status():
#     return JSONResponse(content={"message": "Success"}, status_code=201)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         app,
#         host=os.getenv("FLASK_HOST", "0.0.0.0"),
#         port=int(os.getenv("FLASK_PORT", "8080")),
#         reload=os.getenv("FLASK_DEBUG", "False") == "True"
#     )






# server.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import timedelta

from .auth import auth_router
from .complaint import complaint_router
from .database import Base, engine
from .models import User, Complaint

app = FastAPI()

# CORS Configuration - Fix the issues
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
environment = os.environ.get("ENVIRONMENT", "development")

# Base allowed origins
allowed_origins = [
    frontend_url,
    "https://rail-management-system-v1ju.vercel.app",  # Your exact Vercel URL
]

# Add development origins
if environment != "production":
    allowed_origins.extend([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ])

print(f"Allowed CORS origins: {allowed_origins}")  # Debug log

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-CSRF-TOKEN",
        "x-csrf-token",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
    ],
    expose_headers=["*"],
    max_age=3600,
)

# Create tables
Base.metadata.create_all(bind=engine)

# Add a root endpoint for health check
@app.get("/")
async def root():
    return JSONResponse(content={"message": "Rail Management System API", "status": "running"}, status_code=200)

# Status endpoint
@app.get("/status")
async def status():
    return JSONResponse(content={"message": "Success"}, status_code=200)  # Changed from 201 to 200

# Add OPTIONS handler for preflight requests
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return JSONResponse(
        content={"message": "OK"},
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(complaint_router, prefix="/complaints", tags=["Complaints"])

# Add middleware for additional CORS headers (backup)
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    origin = request.headers.get("origin")
    
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),  # Render uses PORT, not FLASK_PORT
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )