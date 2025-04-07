from flask import Blueprint, request, redirect, render_template, make_response, session
from .models import User
from flask_jwt_extended import create_refresh_token, create_access_token 
from flask import jsonify

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

        return redirect("/auth/login")

    return render_template("signup.html")



@auth_bp.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        user = User.get_user_by_email(email)

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            response = make_response(redirect("/"))  
            response.headers.add("Set-Cookie", f"access_token={access_token}; HttpOnly; Secure; SameSite=Lax")
            response.headers.add("Set-Cookie", f"refresh_token={refresh_token}; HttpOnly; Secure; SameSite=Lax")
            session["name"] = user.name
            session.modified = True

            return response

        return jsonify({"error": "Invalid email or password"}), 401  

    return render_template("login.html") 


@auth_bp.route("/logout", methods=["POST"])
def logout_user():
    response = make_response(redirect("/auth/login")) 
    
    # Clear cookies
    response.headers.add("Set-Cookie", "access_token=; HttpOnly; Secure; SameSite=Lax; Max-Age=0")
    response.headers.add("Set-Cookie", "refresh_token=; HttpOnly; Secure; SameSite=Lax; Max-Age=0")

    session.clear()

    return response 

