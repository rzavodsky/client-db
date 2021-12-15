#!/usr/bin/env python3
from app import db, create_app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
