from flask import Blueprint, redirect, url_for,jsonify, session, current_app
from flask_dance.contrib.google import make_google_blueprint, google
import os
from src.db.core import db
from src.db.models.quiz_db import User as UserModel


auth_bp = Blueprint('auth', __name__)

# google config
google_bp = make_google_blueprint(
    client_id = os.getenv("GOOGLE_CLIENT_ID"),
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET"),
    scope = ["profile","email"],
    redirect_to = "auth.callback"
)

@auth_bp.route("/login")
def login():
    '''redirect to google Oauth'''
    if not google.authorized:
        return redirect(url_for("google.login"))
    return redirect(url_for("auth.callback"))


@auth_bp.route("/callback")
def callback():
    '''handles Oauth callback'''
    if not google.authorized:
        return jsonify({"error": "failed to login"}), 401
    # get user info from google
    user_info = google.get("/oauth2/v3/userinfo")
    if not user_info.ok:
        return jsonify({"error": "failed to get user info"}), 401
    google_info = user_info.json()
    email = google_info.get("email")
    name = google_info.get("name")

    # find or create user
    user_record = UserModel.query.filter_by(name=name, email=email).first()
    try:
        if not user_record:
            user_record = UserModel(name=name, email=email)
            db.session.add(user_record)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    # store user info in session
    session["user_id"] = user_record.id
 

    return jsonify({"success": True, "user": {
    "id": user_record.id,
    "name": user_record.name
    }}), 200
