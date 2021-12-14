#!/usr/bin/env python3
from flask import Flask, request, abort, make_response
from jsonschema import ValidationError
from flask_sqlalchemy import SQLAlchemy

# Routes

db = SQLAlchemy()

### Error Handling ###

# All requests must be JSON
def check_json():
    request.on_json_loading_failed = on_json_loading_failed
    if request.content_length and request.content_length > 0 and not request.is_json:
        return {"error": "Requests must be JSON"}, 400

def on_json_loading_failed(_e):
    abort(make_response({"error": "Can't parse JSON"}, 400))

def handle_client_not_found(e):
    return {"error": f"Client {e.client_id} not found"}

def handle_contact_not_found(e):
    return {"error": f"Contact {e.contact_id} was not found under client {e.client_id}"}

def handle_key_not_found(e):
    return {"error": f"Key {e.key} was not found"}

def handle_validation_error(e: ValidationError):
    return {"error": e.message}, 400 # Bad Request

def create_app():
    from contact.routes import contacts, ContactNotFoundException
    from client.routes import clients, ClientNotFoundException
    from auth.routes import auth, KeyNotFoundException
    from bloky.routes import bloky
    app = Flask(__name__)

    #DB Config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlalchemy_sqlany://DBA:SQL@localhost"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": { "Server": "sqlserver17" }
    }

    # Register functions
    app.before_request(check_json)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(ClientNotFoundException, handle_client_not_found)
    app.register_error_handler(ContactNotFoundException, handle_contact_not_found)
    app.register_error_handler(KeyNotFoundException, handle_key_not_found)

    # Register blueprints
    app.register_blueprint(clients, url_prefix="/clients")
    app.register_blueprint(contacts, url_prefix="/clients/<int:client_id>/contacts")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(bloky, url_prefix="/blocks")

    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug = True)
