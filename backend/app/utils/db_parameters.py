"""Utility functions to initialize database parameters"""

import os


DB_NAME = os.environ.get("DB_NAME")
USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
SCHEMA = os.environ.get("DB_SCHEMA")
HOST = os.environ.get("DB_HOST")
PORT = os.environ.get("DB_PORT")
