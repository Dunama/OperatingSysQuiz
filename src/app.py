from flask import Flask
from flask_migrate import Migrate
from src.config import Config
from src.db.core import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Init db
    db.init_app(app)
    Migrate(app, db)


    with app.app_context():
        # Import models
        from src.db.models.quiz_db import Pat, Questions, Options, Answers, Response
    

        # Import blueprints
        from src.api.models.pat import pat_bp
        from src.api.models.quiz_route import quiz_bp

        # register blueprints
        app.register_blueprint(pat_bp)
        app.register_blueprint(quiz_bp)


    return app

app=create_app()

if __name__ == '__main__':
    app.run(debug=True)