import sys
import os

# Assuming flask_app.wsgi is in the same directory as flask_app.py
current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_directory)

from flask_app import app as application
