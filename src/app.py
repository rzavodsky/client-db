#!/usr/bin/env python3
from flask import Flask, request, abort, make_response
from psycopg2.errors import UniqueViolation
from peewee import ProgrammingError
from jsonschema import ValidationError

from db import db, Client, Contact, client_types, IntegrityError, DoesNotExist

# Routes
from contact_routes import contacts
from client_routes import clients

app = Flask(__name__)


### Error Handling ###

# All requests must be JSON
@app.before_request
def check_json():
    request.on_json_loading_failed = on_json_loading_failed
    if request.method not in ["GET", "DELETE"] and not request.is_json:
        return {"error": "Requests must be JSON"}, 400

def on_json_loading_failed(e):
    abort(make_response({"error": "Can't parse JSON"}, 400))

@app.errorhandler(DoesNotExist)
def handle_item_not_exist(e: DoesNotExist):
    model = str(e).split('>')[0].split(' ')[-1] # Get model name from error message
    return {"error": f"{model} not found"}, 404 # Not Found

@app.errorhandler(IntegrityError)
def handle_duplicate_field(e: IntegrityError):
    if isinstance(e.orig, UniqueViolation) and "ico" in str(e.orig):
        return {"error": "ico already exists in the database"}, 409 # Conflict

@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    return {"error": e.message}, 400 # Bad Request


def setup_database():
    with db.database:
        try:
            enum_fields = ", ".join(f"'{field}'" for field in client_types)
            db.database.execute_sql(f"CREATE TYPE e_type AS ENUM ({enum_fields})")
        except ProgrammingError:
            # Type already exists
            pass
        db.database.create_tables([Client, Contact])


def create_app():
    app.config["DATABASE"] = {
        "name": "postgres",
        "engine": "playhouse.pool.PooledPostgresqlDatabase",
        "user": "postgres",
        "password": "postgres",
        "autorollback": True,
        "host": "db",
        "max_connections": 32,
        "stale_timeout": 600,
    }

    app.register_blueprint(clients, url_prefix="/clients")
    app.register_blueprint(contacts, url_prefix="/clients/<int:client_id>/contacts")

    db.init_app(app)
    setup_database()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug = True)
