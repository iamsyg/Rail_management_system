from flask import Blueprint, request, redirect, render_template
from models import User 

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup_user():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")

        if not name or not email or not password:
            return "Missing fields", 400 

        existing_user = User.get_user_by_email(email)
        if existing_user:
            return "User already exists", 409  

        new_user = User(name=name, email=email)
        new_user.set_password(password)  
        new_user.save()

        return redirect("/")

    return render_template("signup.html")
