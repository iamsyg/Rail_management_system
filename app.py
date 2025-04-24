import threading
import subprocess
from flask import Flask, request
from website.app.pages.api.user.server import app as flask_app  # Import Flask app
from website.app.pages.api.user.auth import get_logged_in_user  
import requests


# def get_logged_in_user():
#     try:
#         access_token = request.cookies.get("access_token")
#         response = requests.get("http://localhost:8080/pages/api/user/profile", 
#                                 cookies={"access_token": access_token})

#         if response.status_code == 200:
#             user_data = response.json()["user"]
#             print("✅ Logged-in user details:", user_data)
#             return user_data
#         else:
#             print("❌ Failed to get user:", response.json())
#     except Exception as e:
#         print("❌ Error fetching user:", e)
#     return None

# user_data = get_logged_in_user()
# print(user_data["name"])


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
