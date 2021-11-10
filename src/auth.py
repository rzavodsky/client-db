import secrets
from hashlib import sha256
from flask import request

from db import db, ApiKey, ApiPermission
from schema_validation import perm_routes

def generate_key():
    """Generates a new 32-byte token"""
    return secrets.token_urlsafe(32)

def hash_key(key: str):
    """Return a hash of a key which can be stored in a database"""
    return sha256(key.encode('utf-8')).hexdigest()


def require_auth(route: str, level: int):
    """Decorator that will make the request require an api authentication
    route -- The route that needs authorization
    level -- The key needs at least this level to access this route"""
    assert route in perm_routes, f"Route {route} is not in the perm_routes list"

    def require_auth_inner(fn):
        def wrapper(*args, **kwargs):
            key = request.headers.get("Authorization")
            if not key or not key.startswith("Bearer "):
                return "", 401 # Unauthorized
            key = key.removeprefix("Bearer ")

            key_inst = db.session.query(ApiKey, ApiPermission).filter(ApiKey.id == ApiPermission.key_id,
                                                                      ApiKey.key == hash_key(key),
                                                                      ApiPermission.route == route,
                                                                      ApiPermission.level >= level).scalar()
            if not key_inst:
                if ApiKey.query.filter(ApiKey.key == hash_key(key)).scalar():
                    # Key exists, but doesn't have necessary permissions
                    return "", 403 # Forbidden
                else:
                    # Key doesn't exist
                    return "", 401 # Unauthorized

            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__ # Change name of wrapper function so flask doesn't complain
        return wrapper
    return require_auth_inner
