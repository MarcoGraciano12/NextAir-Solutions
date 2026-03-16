"""
Day resource endpoints.

REST API resources for day operations (read-only lookup table).

Author: Marco Graciano
Date: 2026-03-13
"""

from models import DayModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import DaySchema

blp = Blueprint("Days", __name__, description="Day lookup operations")


@blp.route("/days")
class DayCollection(MethodView):
    """
    Resource for day collection operations.
    """

    @blp.response(200, DaySchema(many=True))
    def get(self):
        """
        Get all days.

        :return: List of all days (7 days)
        """
        return DayModel.get_all()


@blp.route("/days/<int:day_id>")
class DayItem(MethodView):
    """
    Resource for individual day operations.
    """

    @blp.response(200, DaySchema)
    def get(self, day_id):
        """
        Get a day by ID.

        :param day_id: Day ID (1-7)
        :return: Day data
        """
        day = DayModel.find_by_id(day_id)
        if not day:
            abort(404, message="Day not found.")
        return day
