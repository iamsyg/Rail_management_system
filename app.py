import os
import sys

# Handle NLTK downloads for production deployment
def setup_nltk_for_production():
    """Setup NLTK for production environment"""
    try:
        import nltk
        
        # Set up NLTK data directory in a writable location
        nltk_data_dir = '/tmp/nltk_data'
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)
        
        # Add to NLTK data path
        if nltk_data_dir not in nltk.data.path:
            nltk.data.path.append(nltk_data_dir)
        
        # Download required resources
        resources = ['stopwords', 'punkt', 'wordnet']
        for resource in resources:
            try:
                nltk.data.find(f'corpora/{resource}' if resource != 'punkt' else f'tokenizers/{resource}')
            except LookupError:
                print(f"Downloading NLTK {resource}...")
                nltk.download(resource, download_dir=nltk_data_dir, quiet=True)
                
        print("NLTK setup completed successfully")
        
    except Exception as e:
        print(f"Error setting up NLTK: {e}")
        print("Continuing without NLTK - using fallback text processing")

# Run setup if this looks like a production environment
if os.getenv('RENDER') or os.getenv('PORT') or '/opt/render' in os.getcwd():
    setup_nltk_for_production()







import threading
import subprocess
import os
from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from dotenv import load_dotenv

# Import your existing modules - adjust these imports according to your actual structure
try:
    # These imports should be adjusted to match your FastAPI server structure
    from website.app.pages.api.user.server import app as fastapi_app
    from website.app.pages.api.user.auth import auth_router, get_logged_in_user  
    from website.app.pages.api.user.complaint import complaint_router
    from database.lib.prisma import prisma  # If using Prisma
except ImportError as e:
    print(f"Import error: {e}")
    # Create placeholders if imports fail
    auth_router = None
    complaint_router = None
    prisma = None

# Load environment variables
load_dotenv()

# Initialize main FastAPI app
app = FastAPI()

# Setup CORS
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url] if frontend_url != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-CSRF-TOKEN", "x-csrf-token"],
)

# Register routers from your existing FastAPI app
if auth_router:
    app.include_router(auth_router, prefix="/auth")
if complaint_router:
    app.include_router(complaint_router, prefix="/complaints")

# Root endpoint
@app.get("/", response_class=PlainTextResponse)
async def home():
    return "FastAPI is running!"

# Status endpoint
@app.get("/status")
async def status():
    return {"message": "Success", "status": "online"}

# Database connection management
@app.on_event("startup")
async def startup():
    print("[API] Starting up...")
    if prisma:
        try:
            print("[Prisma] Connecting Prisma client...")
            await prisma.connect()
        except Exception as e:
            print(f"[Prisma] Error connecting: {str(e)}")

@app.on_event("shutdown")
async def shutdown():
    if prisma and prisma.is_connected():
        print("[Prisma] Disconnecting Prisma client...")
        await prisma.disconnect()

# Function to run Next.js
def run_nextjs():
    try:
        # `shell=True` is important on Windows to run npm correctly
        subprocess.call("npm run dev", cwd="website", shell=True)
    except FileNotFoundError as e:
        print("❌ Error launching Next.js app:", e)

# This is only for local development
if __name__ == "__main__":
    import uvicorn
    
    # Start Next.js in a separate thread
    threading.Thread(target=run_nextjs).start()
    
    # Run FastAPI app
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)