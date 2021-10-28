#!/usr/bin/env python3
from flask import Blueprint, request, abort, make_response
from jsonschema import ValidationError

from db import db, Client
from schema_validation import ClientValidator, ClientPATCHValidator
from auth import require_auth

clients = Blueprint("clients", __name__)

@clients.route("")
@require_auth("client", 1)
def get_all_clients():
    if request.args.get("q"):
        query = request.args.get("q")
        clients = Client.query.filter(Client.name.ilike(f"%{query}%"))
    else:
        clients = Client.query.all()
    return {"data": [client.as_dict() for client in clients]}

@clients.route("/<int:client_id>")
@require_auth("client", 1)
def get_single_client(client_id: int):
    client = Client.query.get(client_id)
    if not client:
        raise ClientNotFoundException(client_id)
    return client.as_dict()

@clients.route("", methods = ["POST"])
@require_auth("client", 2)
def add_client():
    body = request.json
    ClientValidator.validate(body)
    client = Client(**body)
    db.session.add(client)
    db.session.commit()
    return client.as_dict()


@clients.route("/<int:client_id>", methods = ["PUT"])
@require_auth("client", 2)
def update_client(client_id: int):
    body = request.json
    ClientValidator.validate(body)
    client = Client.query.get(client_id)
    if not client:
        raise ClientNotFoundException(client_id)

    for col, value in body.items():
        setattr(client, col, value)

    db.session.commit()
    return client.as_dict()

@clients.route("/<int:client_id>", methods = ["PATCH"])
@require_auth("client", 2)
def partial_update_client(client_id: int):
    body = request.json
    ClientPATCHValidator.validate(body)
    client = Client.query.get(client_id)
    if not client:
        raise ClientNotFoundException(client_id)

    for col, value in body.items():
        setattr(client, col, value)

    db.session.commit()
    return client.as_dict()

@clients.route("/<int:client_id>", methods = ["DELETE"])
@require_auth("client", 2)
def delete_client(client_id: int):
    client = Client.query.get(client_id)
    if not client:
        raise ClientNotFoundException(client_id)
    db.session.delete(client)
    db.session.commit()
    return "", 204 # No Content

class ClientNotFoundException(Exception):
    """Raised when a Client wasn't found in the database"""
    def __init__(self, client_id):
        self.client_id = client_id
