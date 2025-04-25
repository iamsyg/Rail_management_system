import threading
import subprocess
from flask import Flask, request
from website.app.pages.api.user.server import app as flask_app , db # Import Flask app
from website.app.pages.api.user.auth import get_logged_in_user  
import requests

from website.app.pages.api.user.models import Complaint,User
from flask_jwt_extended import jwt_required, get_jwt_identity

def run_nextjs():
    try:
        # `shell=True` is important on Windows to run npm correctly
        subprocess.call("npm run dev", cwd="website", shell=True)
    except FileNotFoundError as e:
        print("❌ Error launching Next.js app:", e)

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask API is running!"

if __name__ == "__main__":
    threading.Thread(target=run_nextjs).start()
    flask_app.run(debug=True, port=8080)
