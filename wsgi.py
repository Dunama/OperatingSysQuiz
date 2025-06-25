import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Suppress SQLAlchemy typing warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*TypingOnly.*")

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()