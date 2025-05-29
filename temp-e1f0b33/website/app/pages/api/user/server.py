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

frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [frontend_url]
    
    # Add common domains for development
if os.environ.get("ENVIRONMENT") != "production":
    allowed_origins.extend([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000"
    ])

# CORS config
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

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router, prefix="/auth")
app.include_router(complaint_router, prefix="/complaints")

@app.get("/status")
async def status():
    return JSONResponse(content={"message": "Success"}, status_code=201)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", "8080")),
        reload=os.getenv("FLASK_DEBUG", "False") == "True"
    )
