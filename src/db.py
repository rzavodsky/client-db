#!/usr/bin/env python3
from peewee import *

db = PostgresqlDatabase("postgres", user = "postgres", password = "postgres", host = "db")

class BaseModel(Model):
    '''Base model that uses the Postgres db. All other models should extend this'''
    class Meta:
        database = db

client_types = ['pravnicka_osoba', 'fyzicka_osoba']
class TypeField(Field):
    '''Peewee doesn't support Postgres Enums, so this custom field is a way to let Peewee use the e_type enum.
    The enum itself needs to be created manually in app.py when connecting to the database'''
    field_type = "e_type"


class Client(BaseModel):
    name    = TextField()
    address = TextField()
    ico     = TextField(unique=True)
    type    = TypeField()


class Contact(BaseModel):
    client       = ForeignKeyField(Client, backref="contacts")
    name         = TextField()
    phone_number = TextField()
    email        = TextField()
    address      = TextField()
