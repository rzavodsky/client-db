#!/usr/bin/env python3
from app import db

class Client(db.Model):
    __tablename__ = "klienti"

    id      = db.Column("klient_id", db.Integer, primary_key=True)
    name    = db.Column("knazov", db.String, nullable=False)
    ico     = db.Column("kico", db.String, nullable=False)
    zruseny = db.Column(db.String, nullable=False, default=0)

    contacts = db.relationship("Contact", back_populates="client")

    def as_dict(self):
        columns = ["id", "name", "ico"] # Columns that should be included in the conversion
        return {name: getattr(self, name) for name in columns}
