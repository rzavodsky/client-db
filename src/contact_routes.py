#!/usr/bin/env python3
from flask import Blueprint, request

from client_routes import ClientNotFoundException
from db import db, Client, Contact
from schema_validation import ContactValidator, ContactPATCHValidator
from auth import require_auth

contacts = Blueprint('contacts', __name__)

@contacts.route("")
@require_auth
def get_all_contacts(client_id):
    client = Client.query.get(client_id)
    if client is None:
        raise ClientNotFoundException(client_id)
    if request.args.get("q"):
        query = request.args.get("q")
        contacts = Contact.query.filter(Contact.name.ilike("%{query}%"), Contact.client_id == client_id)
    else:
        contacts = client.contacts
    return { "data": [contact.as_dict() for contact in contacts] }

@contacts.route("/<int:contact_id>")
@require_auth
def get_single_contact(client_id, contact_id):
    contact = Contact.query.filter(Contact.client_id == client_id, Contact.id == contact_id).first()
    if contact is None:
        raise ContactNotFoundException(contact_id, client_id)
    return contact.as_dict()

@contacts.route("", methods = ["POST"])
@require_auth
def add_contact(client_id):
    client = Client.query.get(client_id)
    if not client:
        raise ClientNotFoundException(client_id)
    body = request.json
    ContactValidator.validate(body)
    contact = Contact(client_id=client.id, **body)
    db.session.add(contact)
    db.session.commit()
    return contact.as_dict()

@contacts.route("/<int:contact_id>", methods = ["PUT"])
@require_auth
def update_contact(client_id, contact_id):
    body = request.json
    ContactValidator.validate(body)
    contact = Contact.query.filter(Contact.client_id == client_id, Contact.id == contact_id).first()
    if not contact:
        raise ContactNotFoundException(contact_id, client_id)

    for col, value in body.items():
        setattr(contact, col, value)

    db.session.commit()
    return contact.as_dict()

@contacts.route("/<int:contact_id>", methods = ["PATCH"])
@require_auth
def partial_update_contact(client_id, contact_id):
    body = request.json
    ContactPATCHValidator.validate(body)
    contact = Contact.query.filter(Contact.client_id == client_id, Contact.id == contact_id).first()
    if not contact:
        raise ContactNotFoundException(contact_id, client_id)

    for col, value in body.items():
        setattr(contact, col, value)

    db.session.commit()
    return contact.as_dict()

@contacts.route("/<int:contact_id>", methods = ["DELETE"])
@require_auth
def delete_contact(client_id, contact_id):
    contact = Contact.query.filter(Contact.client_id == client_id, Contact.id == contact_id).first()
    if not contact:
        raise ContactNotFoundException(contact_id, client_id)
    db.session.delete(contact)
    db.session.commit()
    return "", 204 # No Content

class ContactNotFoundException(Exception):
    """Raised when a Contact wasn't found in the database under a specific Client"""
    def __init__(self, contact_id, client_id):
        self.contact_id = contact_id
        self.client_id = client_id
