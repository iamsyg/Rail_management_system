from flask import Flask, render_template, session, redirect
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

if __name__ == "__main__":
    app.run(debug=True)