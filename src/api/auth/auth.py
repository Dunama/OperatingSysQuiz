from flask import Blueprint, redirect, url_for, render_template, session
from authlib.integrations.flask_client import OAuth
import json
import os

auth_bp = Blueprint('auth', __name__)
appConfig = {
    "OAUTH2_CLIENT_ID": os.getenv("OAUTH2_CLIENT_ID"),
    "OAUTH2_CLIENT_SECRET": os.getenv("OAUTH2_CLIENT_SECRET"),
    "OAUTH2_METADATA_URL": os.getenv("OAUTH2_METADATA_URL")
}

oauth = OAuth()


def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        "myApp",
        client_id=appConfig.get("OAUTH2_CLIENT_ID"),
        client_secret=appConfig.get("OAUTH2_CLIENT_SECRET"),
        server_metadata_url=appConfig.get("OAUTH2_METADATA_URL"),
        client_kwargs={
            "scope": "openid email profile"
        }
    )

@auth_bp.route('/')
def home():
    return render_template('signup.html', session=session.get("user"),
                           pretty = json.dumps(session.get("user"), indent=4))


@auth_bp.route("/google-login")
def googleLogin():
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("auth.googleCallback", _external=True))        


@auth_bp.route("/signin-google")
def googleCallback():
    token = oauth.myApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("auth.home"))

@auth_bp.route('/login')
def login():
    return render_template('login.html')

