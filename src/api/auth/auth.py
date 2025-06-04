from flask import Blueprint, redirect, url_for, jsonify, session, current_app, render_template
from flask_dance.contrib.google import make_google_blueprint, google
import os
from src.db.core import db
from src.db.models.quiz_db import User as UserModel


auth_bp = Blueprint('auth', __name__)

# Google config 
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="auth.callback"  # Redirect to your callback route
)

@auth_bp.route("/signup")
def signup():
    try:
        if google.authorized:
            return redirect(url_for("auth.callback"))
        return render_template('signup.html')
    except Exception as e:
        current_app.logger.error(f"Signup error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login")
def login():
    try:
        if not google.authorized:
            return redirect(url_for("google.login"))
        return redirect(url_for("auth.callback"))
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/callback")
def callback():
    try:
        if not google.authorized:
            current_app.logger.error("Google not authorized in callback")
            return jsonify({"error": "failed to login"}), 401
            
        # Get user info from Google
        user_info = google.get("/oauth2/v3/userinfo")
        if not user_info.ok:
            current_app.logger.error(f"Failed to get user info: {user_info.text}")
            return jsonify({"error": "failed to get user info"}), 401
            
        google_info = user_info.json()
        email = google_info.get("email")
        name = google_info.get("name")
        
        if not email or not name:
            return jsonify({"error": "Invalid user info from google"}), 400

        # Find or create user
        user_record = UserModel.query.filter_by(email=email).first()
        try:
            if not user_record:
                user_record = UserModel(name=name, email=email)
                db.session.add(user_record)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Database error: {str(e)}")
            return jsonify({"error": f"Database error: {str(e)}"}), 500

        # Store user info in session
        session["user_id"] = user_record.id
     
        return jsonify({
            "success": True, 
            "user": {
                "id": user_record.id,
                "name": user_record.name
            }
        }), 200
            
    except Exception as e:
        current_app.logger.error(f"Callback error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500