#!/usr/bin/env python3
from app import db

class Contact(db.Model):
    __tablename__ = "klient_kontakt"

    id           = db.Column("kkontakt_id", db.Integer, primary_key=True)
    client_id    = db.Column("kklient_id", db.Integer, db.ForeignKey("klienti.klient_id"))
    name         = db.Column("kkmeno", db.String, nullable=False)
    phone_number = db.Column("kktel", db.String)
    email        = db.Column("kkemail", db.String)

    client = db.relationship("Client", back_populates="contacts")

    def as_dict(self):
        columns = ["id", "client_id", "name", "phone_number", "email"] # Columns that should be included in the conversion
        return {name: getattr(self, name) for name in columns}
