"""
Very jank badge implementation, but i dont think its too bad tbh...
"""

from flask import Blueprint, request
import os

bp = Blueprint(__name__, __name__)

# Badges
def list_badges():
	# TODO: Allow to organise badges into groups
	badge_files = sorted(os.listdir("static/badges"))
	badges = []
	
	for f in badge_files:
		badges.append({"id": int(f.removesuffix(".png")), "icon_url": f"http://{request.host}/static/badges/{f}"})
	
	return {
		"success": True,
		"list": [
			{
				"name": "General",
				"badges": badges,
			}
		],
	}

@bp.get("/<int:version>/<appname>/badges")
def badges(version, appname):
	return list_badges()

@bp.get("/<int:version>/<appname>/users/<int:user_id>/badges")
def user_badges(version, appname, user_id):
	return list_badges()
