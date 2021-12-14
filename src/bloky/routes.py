from flask import Blueprint, request

from bloky.model import Plan, Blok
from bloky.utils import datestring_to_days
from app import db

bloky = Blueprint("bloky", __name__)

@bloky.route("")
def get_all_blocks():
    date = request.args.get("date")
    channel = request.args.get("channel")

    if date is None or channel is None:
        return {"error": "date and channel parameters are required"}, 400

    try:
        date = datestring_to_days(date)
    except ValueError:
        return {"error": "date doesn't match format '%d.%m.%Y'"}, 400

    plans = db.session.query(Plan, Blok).filter(Plan.date == date, Blok.channel == channel, Plan.block_id == Blok.id).all()
    return {
        "data": [plan.as_dict() for (plan, _block) in plans]
    }
