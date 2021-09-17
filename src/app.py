#!/usr/bin/env python3
from flask import Flask, request

# Routes
from contact_routes import contacts
from client_routes import clients

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(clients)
    app.register_blueprint(contacts)
    app.run(host="0.0.0.0", port=5000, debug = True)
