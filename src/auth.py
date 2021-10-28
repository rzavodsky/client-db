import secrets
from flask import request
from db import db, ApiKey, ApiPermission

def generate_key():
    """Generates a new 32-byte token"""
    return secrets.token_urlsafe(32)

def require_auth(route: str, level: int):
    """Decorator that will make the request require an api authentication
    route -- The route that needs authorization
    level -- The key needs at least this level to access this route"""
    def require_auth_inner(fn):
        def wrapper(*args, **kwargs):
            key = request.headers.get("Authorization")
            if not key or not key.startswith("Bearer "):
                return "", 401 # Unauthorized
            key = key.removeprefix("Bearer ")

            key_inst = db.session.query(ApiKey, ApiPermission).filter(ApiKey.id == ApiPermission.key_id,
                                                                      ApiKey.key == key,
                                                                      ApiPermission.route == route,
                                                                      ApiPermission.level >= level).scalar()
            if not key_inst:
                if ApiKey.query.filter(ApiKey.key == key):
                    # Key exists, but doesn't have necessary permissions
                    return "", 403 # Forbidden
                else:
                    # Key doesn't exist
                    return "", 401 # Unauthorized

            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__ # Change name of wrapper function so flask doesn't complain
        return wrapper
    return require_auth_inner
