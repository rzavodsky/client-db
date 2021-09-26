#!/usr/bin/env python3
from flask import Blueprint

contacts = Blueprint('contacts', __name__)

@contacts.route("")
def get_all_contacts(client_id):
    pass

@contacts.route("/<int:contact_id>")
def get_single_contact(client_id, contact_id):
    pass

@contacts.route("", methods = ["POST"])
def add_contact(client_id):
    pass

    pass
@contacts.route("/<int:contact_id>", methods = ["PUT"])
def update_contact(client_id, contact_id):

    pass
@contacts.route("/<int:contact_id>", methods = ["PATCH"])
def partial_update_contact(client_id, contact_id):

    pass
@contacts.route("/<int:contact_id>", methods = ["DELETE"])
def delete_contact(client_id, contact_id):
