from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from src.config import Config
from src.db.core import db
from sqlalchemy import MetaData

def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')
    app.config.from_object(Config)
    
    # Add naming convention for constraints (fixes migration issues)
    convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    
    metadata = MetaData(naming_convention=convention)
    db.metadata = metadata
    
    # Init db
    db.init_app(app)
    migrate = Migrate(app, db)
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    with app.app_context():
        # Import models
        from src.db.models.quiz_db import User, Questions, Options, Answers, Response

        # Import blueprints
        from src.api.models.quiz_route import quiz_bp
        from src.api.models.demoRun import demo_bp
        from src.api.models.practiceQuiz import practice_bp
        from src.api.models.questionBank import comprehensive_bp
        from src.api.auth.auth import auth_bp, google_bp

        # register blueprints
        app.register_blueprint(quiz_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(demo_bp)
        app.register_blueprint(practice_bp)
        app.register_blueprint(comprehensive_bp)
        app.register_blueprint(google_bp)

    return app

# For Vercel
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)