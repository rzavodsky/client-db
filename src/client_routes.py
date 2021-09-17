#!/usr/bin/env python3
from flask import Blueprint

clients = Blueprint("clients", __name__)

@clients.route("/clients")
def get_all_clients():
    pass

@clients.route("/clients/<client_id>")
def get_single_client(client_id):
    pass

@clients.route("/clients", methods = ["POST"])
def add_client():
    pass

@clients.route("/clients/<client_id>", methods = ["PUT"])
def update_client():
    pass

@clients.route("/clients/<client_id>", methods = ["PATCH"])
def partial_update_client():
    pass

@clients.route("/clients/<client_id>", methods = ["DELETE"])
def delete_client():
    pass
