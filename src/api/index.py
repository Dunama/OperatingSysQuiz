import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__, '..', 'src')))

from src.app import app

# This is the entry point for Vercel
def handler(event, context):
    return app(event, context)

# Also export app for Vercel
if __name__ == "__main__":
    app.run()