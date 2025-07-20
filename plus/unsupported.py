"""
This file contains the error implementation for features that will _never_ be
implemented in Katten server. This is most likely because they are no longer
useful (e.g. rely on dead external services or APIs).
"""

from flask import Blueprint
from utils import *

bp = Blueprint(__name__, __name__)

@bp.post("/users/update_social_photo") # Dependent on social media services
@bp.get("/challenges/<int:id>") # AFAIK challenges require push notifications
@bp.post("/challenges")
@bp.get("/challenges")
@bp.put("/challenges/<int:id>")
def error(*args, **kwargs):
	plus_error(400, "Katten does not support this feature")

