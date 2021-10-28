from flask import Blueprint
from db import db, ApiKey
from auth import generate_key, require_auth

auth = Blueprint("auth", __name__)

@auth.route("")
@require_auth
def get_all_keys():
    return {"data": [key.as_dict() for key in ApiKey.query.all()] }

@auth.route("/<string:key>")
def get_by_key(key):
    key_inst = ApiKey.query.filter(ApiKey.key == key).first()
    if not key_inst:
        raise KeyNotFoundException(key)
    return key_inst.as_dict()

@auth.route("", methods = ["POST"])
@require_auth
def create_new_key():
    key = ApiKey(key = generate_key())
    db.session.add(key)
    db.session.commit()
    return key.as_dict()

@auth.route("/<int:key_id>", methods = ["DELETE"])
@require_auth
def delete_key(key_id):
    key = ApiKey.query.get(key_id)
    if not key:
        raise KeyNotFoundException(key)
    db.session.delete(key)
    db.session.commit()
    return "", 204 # No Content

class KeyNotFoundException(Exception):
    """Raised when a requested key is not found in the database"""
    def __init__(self, key):
        self.key = key
