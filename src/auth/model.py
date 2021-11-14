#!/usr/bin/env python3
from app import db

class ApiKey(db.Model):
    __tablename__ = "api_kluce"

    id                    = db.Column("id", db.Integer, primary_key=True)
    key                   = db.Column("kluc", db.String, unique=True)

    perms = db.relationship("ApiPermission", back_populates="key", cascade="all,delete-orphan")

    def as_dict(self):
        # This is used to fill all routes that this key doesn't have permissions for with 0
        zero_perms = {route: 0 for route in perm_routes}
        actual_perms = {perm.route: perm.level for perm in self.perms}
        return {
            "id": self.id,
            "permissions": {**zero_perms, **actual_perms}
        }

class ApiPermission(db.Model):
    __tablename__ = "api_prava"

    id = db.Column("id", db.Integer, primary_key=True)
    key_id = db.Column("kluc_id", db.Integer, db.ForeignKey("api_kluce.id"))
    route = db.Column("route", db.String, nullable=False)
    level = db.Column("level", db.Integer, nullable=False)

    key = db.relationship("ApiKey", back_populates="perms")
