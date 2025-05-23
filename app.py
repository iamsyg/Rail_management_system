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