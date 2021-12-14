from app import db
from bloky.utils import days_to_datestring

class Blok(db.Model):
    __tablename__ = "bloky"

    id          = db.Column("blok_id", db.Integer, primary_key=True)
    time        = db.Column("brelod", db.Integer)
    floating    = db.Column("bpohyblive", db.Integer)
    block_order = db.Column("bporadie", db.Integer)
    block_type  = db.Column("btyp", db.Integer)
    block_title = db.Column("bpopis", db.String)
    channel     = db.Column("bokruh", db.String)

    def as_dict(self):
        return {field: getattr(self, field) for field in ["time", "floating", "block_order", "block_type", "block_title"]}

class Plan(db.Model):
    __tablename__ = "plan"

    plan_id  = db.Column("plan_id", db.Integer, primary_key=True)
    block_id = db.Column("pblok_id", db.ForeignKey("bloky.blok_id"))
    date     = db.Column("pdd", db.Integer)

    block = db.relationship("Blok")
    spots = db.relationship("PlanProd", back_populates="plan", lazy="joined")

    def as_dict(self) :
        blok = self.block.as_dict()
        return {
            **blok,
            "plan_id": self.plan_id,
            "date": days_to_datestring(self.date),
            "spots": [spot.as_dict() for spot in self.spots],
        }

class PlanProd(db.Model):
    __tablename__ = "plan_prod"

    spot_id      = db.Column("plan_prod_id", db.Integer, primary_key=True)
    spot_order   = db.Column("pporadie", db.Integer)
    spot_address = db.Column("ppadresa", db.ForeignKey("adresy.aadresa"))
    plan_id      = db.Column("pplan_id", db.ForeignKey("plan.plan_id"))
    spot_length  = db.Column("pdlzka", db.Integer)
    broadcasted  = db.Column("podvysielane", db.Integer)

    plan    = db.relationship("Plan", back_populates="spots", lazy="joined")
    address = db.relationship("Adresa", lazy="joined")

    def as_dict(self):
        plan = {field: getattr(self, field) for field in ["spot_order", "spot_id", "spot_length", "spot_address", "broadcasted"]}
        address = self.address.as_dict()

        return {**plan, **address}


class Adresa(db.Model):
    __tablename__ = "adresy"

    adresa        = db.Column("aadresa", db.String, primary_key=True)
    spot_filename = db.Column("afilename", db.String)
    spot_in       = db.Column("ain", db.Integer)
    spot_out      = db.Column("aout", db.Integer)
    spot_duration = db.Column("aduration", db.Integer)

    def as_dict(self):
        return {field: getattr(self, field) for field in ["spot_filename", "spot_in", "spot_out", "spot_duration"]}
