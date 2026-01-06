#!/usr/bin/env python3
"""
Main Application Entry Point for Render Deployment
"""

import os
import sys
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use the simple backend that doesn't require MongoDB
from backend.simple_backend import app

# Export the Flask app for gunicorn
application = app

logger.info("✅ Simple Backend Application created successfully")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print("🚀 MongoDB Backend starting...")
    print(f"🔧 Running on port: {port}")
    print(f"🐛 Debug mode: {debug}")
    print("📊 Database: MongoDB Atlas")

    app.run(host='0.0.0.0', port=port, debug=debug)
