from utils import *
from flask import Blueprint, request

bp = Blueprint(__name__, __name__)

@bp.get("/<int:version>/<appname>/users/<int:user_id>/achievements")
def get_users_achievements(version, appname, user_id):
	return {
		"success": True,
		"user_id": user_id,
		"achievements": [
			{
				"index": 0,
				"points": 0,
				"name": "Achievements not implemented",
				"category": "Katten Server",
				"description": "Achievements are not implemented on Katten Server",
				"icon_url": fallback_icon(),
				"unlocked": True,
			}
		],
	}
