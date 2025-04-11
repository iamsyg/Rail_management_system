from flask import Blueprint, request, redirect, render_template, make_response, session
from .models import User
from flask_jwt_extended import create_refresh_token, create_access_token
from flask import jsonify
from .models import RoleEnum
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, decode_token

def generateAccessTokenAndRefreshToken(userEmail):
    try:
        user = User.get_user_by_email(userEmail)

        if not user :
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        accessToken = user.generate_access_token()
        refreshToken = user.generate_refresh_token()

        user.refresh_token = refreshToken
        user.save()

        return {
            "accessToken": accessToken,
            "refreshToken": refreshToken
        }, None, None

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error generating tokens: {str(e)}"
        })


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup_user():
    if request.method == "POST":
        try:
            # Get and validate form data
            data = request.get_json()
            name = data.get("name", "").strip()
            email = data.get("email", "").strip().lower()
            phoneNumber = data.get("phoneNumber", "").strip()
            password = data.get("password", "").strip()
            
            if not all([name, email, phoneNumber, password]):
                return jsonify({
                    "success": False,
                    "message": "All fields are required",
                    "missing_fields": [
                        field for field, value in [
                            ("name", name),
                            ("email", email), 
                            ("phoneNumber", phoneNumber),
                            ("password", password)
                        ] if not value
                    ]
                }), 400
            
            existing_user = User.get_user_by_email(email)
            if existing_user:
                return jsonify({
                    "success": False,
                    "message": "User with this email already exists"
                }), 409
        
            new_user = User(
                name=name,
                email=email,
                phoneNumber = phoneNumber,
                password = "",
                role = RoleEnum.user
            )

            new_user.set_password(password)

            new_user.save()
            
            return jsonify({
                "success": True,
                "message": "User created successfully",
                "user": {
                    "id": new_user.id,
                    "name": new_user.name,
                    "phoneNumber": new_user.phoneNumber,
                    "email": new_user.email
                }
            }), 201
        
        except Exception as e:
            # Log the error for debugging
            print(f"Error during signup: {str(e)}")
            return jsonify({
                "success": False,
                "message": "An error occurred during signup"
            }), 500
    
    # GET request or other methods
    return jsonify({
        "success": False,
        "message": "Method not allowed",
        "allowed_methods": ["POST"]
    }), 405



@auth_bp.route("/signin", methods=["POST"])
def signin_user():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        user = User.get_user_by_email(email)

        if not user:
            return jsonify({"error": "User not found"}), 401

        if user.check_password(password):

            tokens, error_response, status_code = generateAccessTokenAndRefreshToken(user.email)

            if error_response:
                return error_response, status_code
            
            access_token = tokens["accessToken"]
            refresh_token = tokens["refreshToken"]

            response = jsonify({
                "message": "Login successful",
                "success": True,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phoneNumber": user.phoneNumber,
                    "role": user.role.value
                },
                "accessToken": access_token,
                "refreshToken": refresh_token
            })

            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            # session["name"] = user.name
            # session.permanent = True
            # session.modified = True
            
            return response, 200

        return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        print(f"[ERROR] during login: {str(e)}")
        return jsonify({"error": "An error occurred during login"}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout_user():

    response = jsonify({"message": "Logged out successfully"})
    response.headers.add("Set-Cookie", "access_token=; HttpOnly; Secure; SameSite=Lax; Max-Age=0")
    response.headers.add("Set-Cookie", "refresh_token=; HttpOnly; Secure; SameSite=Lax; Max-Age=0")
    return response, 200

# @auth_bp.route("/profile", methods=["GET"])
# # @jwt_required()
# def get_logged_in_user():
#     identity = request.cookies.get("access_token")
#     print("[DEBUG] identity:", identity)
#     print("[DEBUG] identity from token:", identity)

#     if not identity or not isinstance(identity, dict):
#         return jsonify({"error": "Invalid token payload"}), 401
    
#     return jsonify({
#         "user": identity
#     }), 200

@auth_bp.route("/profile", methods=["GET"])
def get_logged_in_user():
    token = request.cookies.get("access_token")
    if not token:
        return jsonify({"error": "No token found"}), 401

    try:
        decoded = decode_token(token)
        identity = decoded.get("sub")
        print("[DEBUG] identity from token:", identity)
        return jsonify({"user": identity}), 200
    except Exception as e:
        print("Token decode failed:", str(e))
        return jsonify({"error": "Invalid token"}), 401

@auth_bp.route("/refresh", methods=["POST", "GET"])
@jwt_required(refresh=True)
def refresh():
    if request.method != "POST":
        return jsonify({"error": "Method Not Allowed"}), 405
    
    current_user = get_jwt_identity()
    print("[DEBUG] current_user:", current_user)
    access_token = create_access_token(identity=current_user)
    response = jsonify({"access_token": access_token})

    return response, 200

@auth_bp.route("/debug-cookies")
def debug_cookies():
    print("Access Token Cookie:", request.cookies.get("access_token"))
    print("Refresh Token Cookie:", request.cookies.get("refresh_token"))
    return jsonify(success=True)

