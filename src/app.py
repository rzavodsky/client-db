#!/usr/bin/env python3
from flask import Flask, request

from db import db, Client, Contact, client_types
from peewee import ProgrammingError

# Routes
from contact_routes import contacts
from client_routes import clients

app = Flask(__name__)

def create_enum():
    with db.atomic() as transaction:
        try:
            enum_fields = ", ".join(f"'{field}'" for field in client_types)
            db.execute_sql(f"CREATE TYPE e_type AS ENUM ({enum_fields})")
        except ProgrammingError:
            # Type already exists
            pass

if __name__ == "__main__":
    try:
        db.connect()
        # Create the type enum
        create_enum()
        db.create_tables([Client, Contact])

        app.register_blueprint(clients)
        app.register_blueprint(contacts)
        app.run(host="0.0.0.0", port=5000, debug = True)
    finally:
        db.close()
