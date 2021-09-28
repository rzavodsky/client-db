#!/usr/bin/env python3
from flask import Blueprint, request, abort, make_response
from psycopg2.errors import UniqueViolation
from jsonschema import ValidationError

from db import Client, DoesNotExist, IntegrityError
from schema_validation import ClientValidator, ClientPATCHValidator

clients = Blueprint("clients", __name__)

@clients.route("")
def get_all_clients():
    if request.args.get("q"):
        clients = Client.select().where(Client.name.contains(request.args.get("q")))
    else:
        clients = Client.select()
    return {"data": [client.__data__ for client in clients]}

@clients.route("/<int:client_id>")
def get_single_client(client_id: int):
    return Client.get_by_id(client_id).__data__

@clients.route("", methods = ["POST"])
def add_client():
    body = request.json
    ClientValidator.validate(body)
    client = Client.create(**body)
    return client.__data__


@clients.route("/<int:client_id>", methods = ["PUT"])
def update_client(client_id: int):
    body = request.json
    ClientValidator.validate(body)
    client = Client.get_by_id(client_id)
    client.__data__ = {**client.__data__, **body}
    client.save()
    return client.__data__

@clients.route("/<int:client_id>", methods = ["PATCH"])
def partial_update_client(client_id: int):
    body = request.json
    ClientPATCHValidator.validate(body)
    client = Client.get_by_id(client_id)
    client.__data__ = {**client.__data__, **body}
    client.save()
    return client.__data__

@clients.route("/<int:client_id>", methods = ["DELETE"])
def delete_client(client_id: int):
    client = Client.get_by_id(client_id)
    client.delete_instance(recursive=True) # Deletes all related contacts as well
    return "", 204 # No Content
