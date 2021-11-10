from flask import Blueprint, request
from db import db, ApiKey, ApiPermission
from auth import generate_key, require_auth, hash_key
from schema_validation import AuthValidator, perm_routes

auth = Blueprint("auth", __name__)

@auth.route("")
@require_auth("auth", 1)
def get_all_keys():
    return {"data": [key.as_dict() for key in ApiKey.query.all()] }

@auth.route("/<string:key>")
@require_auth("auth", 1)
def get_by_key(key):
    key_inst = ApiKey.query.filter(ApiKey.key == hash_key(key)).first()
    if not key_inst:
        raise KeyNotFoundException(key)
    return key_inst.as_dict()

@auth.route("", methods = ["POST"])
@require_auth("auth", 2)
def create_new_key():
    body = request.json
    AuthValidator.validate(body)

    key = generate_key()
    key_obj = ApiKey(key = hash_key(key))
    for route, level in body["permissions"].items():
        if level > 0:
            key_obj.perms.append(ApiPermission(route=route, level=level))

    db.session.add(key_obj)
    db.session.commit()
    return {**key_obj.as_dict(), "key": key}

@auth.route("/<int:key_id>", methods = ["PUT", "PATCH"])
@require_auth("auth", 2)
def update_key(key_id):
    key = ApiKey.query.get(key_id)
    if not key:
        raise KeyNotFoundException(key_id)

    body = request.json
    AuthValidator.validate(body)

    for route, level in body["permissions"].items():
        perm = ApiPermission.query.filter(ApiPermission.key_id == key_id, ApiPermission.route == route).first()
        if perm:
            perm.level = level
        else:
            key.perms.append(ApiPermission(route=route, level=level))

    db.session.commit()
    return key.as_dict()

@auth.route("/<int:key_id>", methods = ["DELETE"])
@require_auth("auth", 2)
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
