from flask import Flask, render_template, session, redirect, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from .models import db, jwt
from .auth import auth_bp
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.config.from_prefixed_env()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "eternity"
app.config["JWT_SECRET_KEY"] = os.environ.get("FLASK_JWT_SECRET_KEY")

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False  # True if using HTTPS only

app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Set True in production with CSRF handling

app.config["JWT_ACCESS_COOKIE_PATH"] = "/"  # access token valid for all routes
app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"  # very important
app.config["JWT_COOKIE_SAMESITE"] = "Lax"

CORS(
        app,
        origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )

user_bp = Blueprint('user', __name__, url_prefix='/user')

db.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix="/auth")

# @app.route("/")
# def authentication():
#     if "name" not in session: 
#         return False  
#     return jsonify({"name": session["name"]}) 

@app.route("/status", methods=["GET"])
def status():
    # if "name" not in session: 
    #     return jsonify({"message": "Unauthorized"}), 401  
    return jsonify({"message": "Success"}), 201


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has expired", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "message": "Request doesnt contain valid token",
                "error": "authorization_header",
            }
        ),
        401,
    )

if __name__ == "__main__":
    
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", "8080")),
        debug=os.getenv("FLASK_DEBUG", "False") == "True"
    )

# from flask import Flask, jsonify
# from flask_cors import CORS

# app = Flask(__name__)

# CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# @app.route("/status")
# def status():
#     return jsonify({"message": "Success"}), 201

# if __name__ == "__main__":
#     app.run(debug=True, port=8080)