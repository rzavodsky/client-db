import secrets
from flask import request
from db import ApiKey

def generate_key():
    """Generates a new 32-byte token"""
    return secrets.token_urlsafe(32)

def require_auth(fn):
    """Decorator that will make the request require an api authentication"""
    def route():
        key = request.headers.get("Authorization")
        if not key or not key.startswith("Bearer "):
            return "Bad or missing Authorization header", 401
        key = key.removeprefix("Bearer ")
        if not ApiKey.query.filter(ApiKey.key == key).scalar():
            return "Key doesn't exist", 401
        return fn()

    return route
