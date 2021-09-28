#!/usr/bin/env python3
from peewee import *
from playhouse.flask_utils import FlaskDB

db = FlaskDB()

client_types = ['pravnicka_osoba', 'fyzicka_osoba']
class TypeField(Field):
    '''Peewee doesn't support Postgres Enums, so this custom field is a way to let Peewee use the e_type enum.
    The enum itself needs to be created manually in app.py when connecting to the database'''
    field_type = "e_type"


class Client(db.Model):
    name    = TextField()
    address = TextField()
    ico     = TextField(unique=True)
    type    = TypeField()


class Contact(db.Model):
    client_id    = ForeignKeyField(Client, backref="contacts")
    name         = TextField()
    phone_number = TextField()
    email        = TextField()
    address      = TextField()
