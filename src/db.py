#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = "klienti"

    id      = db.Column("klient_id", db.Integer, primary_key=True)
    name    = db.Column("knazov", db.String, nullable=False)
    ico     = db.Column("kico", db.String, nullable=False)
    zruseny = db.Column(db.String, nullable=False)

    def as_dict(self):
        columns = ["id", "name", "ico"] # Columns that should be included in the conversion
        return {name: getattr(self, name) for name in columns}

class Contact(db.Model):
    __tablename__ = "klient_kontakt"

    id           = db.Column("kkontakt_id", db.Integer, primary_key=True)
    client_id    = db.Column("kklient_id", db.Integer, db.ForeignKey("klienti.klient_id"))
    name         = db.Column("kkmeno", db.String, nullable=False)
    phone_number = db.Column("kktel", db.String)
    email        = db.Column("kkemail", db.String)

    def as_dict(self):
        columns = ["id", "client_id", "name", "phone_number", "email"] # Columns that should be included in the conversion
        return {name: getattr(self, name) for name in columns}
