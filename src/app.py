from flask import Flask, render_template
from flask_migrate import Migrate
from src.config import Config
from src.db.core import db
import os

# Import auth_bp and init_oauth BEFORE create_app
from src.api.auth.auth import auth_bp, init_oauth

def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')
    app.config.from_object(Config)
    
    # Initialize the database
    db.init_app(app)
    init_oauth(app)
    # Only create migrate in development
    if not os.getenv("VERCEL_ENV"):
        migrate = Migrate(app, db)
    
    @app.route('/')
    def index():
        return render_template('signup.html')

    with app.app_context():
        # Import models
        from src.db.models.quiz_db import User, Questions, Options, Answers, Response
        # Import blueprints
        from src.api.models.quiz_route import quiz_bp
        from src.api.models.demoRun import demo_bp
        from src.api.models.practiceQuiz import practice_bp
        from src.api.models.questionBank import comprehensive_bp

        # Register blueprints
        app.register_blueprint(quiz_bp)
        app.register_blueprint(demo_bp)
        app.register_blueprint(practice_bp)
        app.register_blueprint(comprehensive_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
    return app   

# For Vercel
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)