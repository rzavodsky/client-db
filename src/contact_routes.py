#!/usr/bin/env python3
from flask import Blueprint

contacts = Blueprint('contacts', __name__)

@contacts.route("/clients/<client_id>/contacts")
def get_all_contacts(client_id):
    pass

@contacts.route("/clients/<client_id>/contacts/<contact_id>")
def get_single_contact(client_id, contact_id):
    pass

@contacts.route("/clients/<client_id>/contacts", methods = ["POST"])
def add_contact(client_id):
    pass

@contacts.route("/clients/<client_id>/contacts", methods = ["PUT"])
def update_contact(client_id):
    pass

@contacts.route("/clients/<client_id>/contacts", methods = ["PATCH"])
def partial_update_contact(client_id):
    pass

@contacts.route("/clients/<client_id>/contacts", methods = ["DELETE"])
def delete_contact(client_id):
    pass
