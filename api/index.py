"""
Vercel Serverless Function Entry Point
Imports the Flask app from the main api.py module
"""

import sys
import os

# Add parent directory to path to import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from api import app

# Vercel expects 'app' or 'handler'
# Flask app is already named 'app' so we're good

