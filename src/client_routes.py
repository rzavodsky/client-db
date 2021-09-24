#!/usr/bin/env python3
from flask import Blueprint, request, abort, make_response
from psycopg2.errors import UniqueViolation
from db import Client, DoesNotExist, IntegrityError
from schema_validation import ClientValidator, ClientPATCHValidator
from jsonschema import ValidationError

clients = Blueprint("clients", __name__)

@clients.route("/clients")
def get_all_clients():
    return {"data": [client.__data__ for client in Client.select()]}

@clients.route("/clients/<int:client_id>")
def get_single_client(client_id: int):
    return Client.get_by_id(client_id).__data__

@clients.route("/clients", methods = ["POST"])
def add_client():
    body = request.json
    ClientValidator.validate(body)
    client = Client.create(**body)
    return client.__data__


@clients.route("/clients/<int:client_id>", methods = ["PUT"])
def update_client(client_id: int):
    body = request.json
    ClientValidator.validate(body)
    client = Client.get_by_id(client_id)
    client.__data__ = {**client.__data__, **body}
    client.save()
    return client.__data__

@clients.route("/clients/<int:client_id>", methods = ["PATCH"])
def partial_update_client(client_id: int):
    body = request.json
    ClientPATCHValidator.validate(body)
    client = Client.get_by_id(client_id)
    client.__data__ = {**client.__data__, **body}
    client.save()
    return client.__data__

@clients.route("/clients/<int:client_id>", methods = ["DELETE"])
def delete_client(client_id: int):
    client = Client.get_by_id(client_id)
    client.delete_instance()
    return "", 204 # No Content


@clients.before_request
def check_json():
    request.on_json_loading_failed = on_json_loading_failed
    if not request.is_json and request.method != "GET":
        return {"error": "Requests must be JSON"}, 400

def on_json_loading_failed(e):
    abort(make_response({"error": "Can't parse JSON"}, 400))

@clients.errorhandler(DoesNotExist)
def handle_client_not_exist(e: DoesNotExist):
    return {"error": "Client not found"}, 404 # Not Found

@clients.errorhandler(IntegrityError)
def handle_duplicate_field(e: IntegrityError):
    if isinstance(e.orig, UniqueViolation) and "ico" in str(e.orig):
        return {"error": "ico already exists in the database"}, 409 # Conflict

@clients.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    return {"error": e.message}, 400 # Bad Request
