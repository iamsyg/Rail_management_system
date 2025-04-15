import threading
import subprocess
from flask import Flask
from website.app.pages.api.user.server import app as flask_app  # Import Flask app

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
