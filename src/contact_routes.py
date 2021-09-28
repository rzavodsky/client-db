#!/usr/bin/env python3
from flask import Blueprint, request
from db import Client, Contact
from schema_validation import ContactValidator, ContactPATCHValidator

contacts = Blueprint('contacts', __name__)

@contacts.route("")
def get_all_contacts(client_id):
    client = Client.get_by_id(client_id)
    if request.args.get("q"):
        contacts = Contact.select().where((Contact.client_id == client_id) & Contact.name.contains(request.args.get("q")))
    else:
        contacts = client.contacts
    return { "data": [contact.__data__ for contact in contacts] }

@contacts.route("/<int:contact_id>")
def get_single_contact(client_id, contact_id):
    contact = Contact.get(id=contact_id, client_id=client_id)
    return contact.__data__

@contacts.route("", methods = ["POST"])
def add_contact(client_id):
    client = Client.get_by_id(client_id)
    data = request.json
    ContactValidator.validate(data)
    contact = Contact.create(client_id=client.id, **data)
    return contact.__data__

@contacts.route("/<int:contact_id>", methods = ["PUT"])
def update_contact(client_id, contact_id):
    body = request.json
    ContactValidator.validate(body)
    contact = Contact.get(id=contact_id, client_id=client_id)
    contact.__data__ = {**contact.__data__, **body};
    contact.save()
    return contact.__data__

@contacts.route("/<int:contact_id>", methods = ["PATCH"])
def partial_update_contact(client_id, contact_id):
    body = request.json
    ContactPATCHValidator.validate(body)
    contact = Contact.get(id=contact_id, client_id=client_id)
    contact.__data__ = {**contact.__data__, **body};
    contact.save()
    return contact.__data__

@contacts.route("/<int:contact_id>", methods = ["DELETE"])
def delete_contact(client_id, contact_id):
    contact = Contact.get(id=contact_id, client_id=client_id)
    contact.delete_instance()
    return "", 204 # No Content
