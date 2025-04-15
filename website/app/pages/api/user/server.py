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

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# app.config["JWT_TOKEN_LOCATION"] = ["headers"]
# app.config["JWT_HEADER_NAME"] = "Authorization"
# app.config["JWT_HEADER_TYPE"] = "Bearer"

app.config["JWT_COOKIE_SECURE"] = False  # True if using HTTPS only

app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
app.config["JWT_COOKIE_CSRF_PROTECT"] = True  # Set True in production with CSRF handling

app.config["JWT_ACCESS_COOKIE_PATH"] = "/"  # access token valid for all routes
app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"  # very important
app.config["JWT_COOKIE_SAMESITE"] = "Lax"

CORS(
        app,
        origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"]
    )

db.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()

user_bp = Blueprint('user', __name__, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/status", methods=["GET"])
def status():  
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