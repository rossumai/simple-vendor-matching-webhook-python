import os

SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "secret")
