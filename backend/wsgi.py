import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Ensure project root is on sys.path when running as a script
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

try:
	from app import create_app  # when backend is a package
except Exception:
	from backend.app import create_app  # when running from project root

application = create_app()

from waitress import serve

if __name__ == "__main__":
    serve(application, host="0.0.0.0", port=5000)
