from flask import Flask, render_template, session, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, jwt
from auth import auth_bp

app = Flask(__name__)
app.config.from_prefixed_env()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SECRET_KEY"] = "eternity"

db.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    if "name" not in session: 
        return redirect("/auth/login")  
    return render_template("index.html")  

@app.route("/status")
def status():
    if "name" not in session: 
        return redirect("/auth/login")  
    return render_template("status.html")


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
    app.run(debug=True)