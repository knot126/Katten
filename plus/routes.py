from flask import Blueprint, Response, request, g, make_response, url_for, abort, redirect
from user import *
from utils import *

bp = Blueprint(__name__, __name__)

# Games
# def list_games(appname):
# 	return {
# 		"success": True,
# 		"games": [
# 			{
# 				"app_key": appname,
# 				"name": appname,
# 				"publisher": "Katten Server",
# 				"category": "unknown",
# 				"featured": False,
# 				"leaderboards_count": 0,
# 				"achievements_count": 0,
# 				"id": 1,
# 				"master_product_id": 1,
# 				"icon_url": f"http://{request.host}/static/badges/0.png",
# 				"app_store_url": "http://example.com/",
# 				"feed_url": "http://example.com/",
# 				"catalog_url": "http://example.com/",
# 				"description": "This is the current game.",
# 				"phone_screenshot_urls": [f"http://{request.host}/static/badges/0.png"],
# 				"phone_thumbnail_urls": [f"http://{request.host}/static/badges/0.png"],
# 				"promotion_image_url": f"http://{request.host}/static/badges/0.png",
# 			}
# 		],
# 	}



# @bp.post("/<int:version>/<appname>/users/<int:user_id>/user_data")
# def user_data_set(version, appname, user_id):
# 	"""
# 	Save a key-value pair; ignores user id for now as it's not possbile to
# 	change someone else's user data atm.
# 	"""
# 	
# 	user = User.current()
# 	data = request.form.to_dict()
# 	
# 	UserAppDataEntry.set(appname, user.get_id(), data["key"], data["privacy"], request.files["value"].read())
# 	
# 	return {
# 		"success": True
# 	}
# 
# @bp.get("/<int:version>/<appname>/users/<int:user_id>/user_data/<key>")
# def user_data_get_one(version, appname, user_id, key):
# 	"""
# 	Get a single value from user data storage
# 	"""
# 	
# 	user = User.current()
# 	data = UserAppDataEntry.get(appname, user.get_id(), key)
# 	
# 	return Response(data, mimetype='application/octet-stream')
# 
# @bp.get("/<int:version>/<appname>/users/<int:user_id>/user_data")
# def user_data_get_keys(version, appname, user_id):
# 	"""
# 	Get a list of keys that are stored for the given user
# 	"""
# 	
# 	user = User.current()
# 	
# 	datas = []
# 	
# 	for entry in UserAppDataEntry.lookup_many({"game": appname, "user": user.get_id()}):
# 		datas.append(entry.key)
# 	
# 	return {
# 		"success": True,
# 		"datas": datas,
# 	}

# @bp.get("/<int:version>/<appname>/user_updates")
# def get_user_updates(version, appname):
# 	user = User.current()
# 	
# 	return {
# 		"success": True,
# 		"online_friends": [],
# 		"updates": [],
# 		"update_interval": PLUS_USER_UPDATE_INTERVAL,
# 	}

# @bp.get("/<int:version>/<appname>/users/<int:user_id>/buddies")
# def users_buddies(version, appname, user_id):
# 	user = User.current()
# 	
# 	return {
# 		"success": True,
# 		"list": [],
# 		"offset": 0,
# 		"total": 0,
# 	}

# @bp.post("/<int:version>/<appname>/session")
# def session_init(version, appname):
# 	# Katten doesn't really care about OAuth 1.0's signing things; it's only
# 	# relevant over an insecure HTTP connection anyway.
# 	
# 	# If there is an auth_token instead of gamertag and password then we're
# 	# logging in using an existing session.
# 	if "auth_token" in request.form:
# 		session = UserSession.lookup({"token": request.form["auth_token"]})
# 		
# 		if not session or not session.validate():
# 			plus_error(401, "Session is not valid")
# 		
# 		user = session.get_user()
# 		
# 		return make_login_response(user, session)
# 	else:
# 		try:
# 			result = User.login(request.form["gamertag"], request.form["password"])
# 			
# 			return make_login_response(result.user, result.session)
# 		except LoginError:
# 			plus_error(1, "Wrong username or password")

# @bp.post("/<int:version>/<appname>/oauth/authorize_new")
# def oauth_authorize_new(version, appname):
# 	"""
# 	This should do something oauth related but we can just return the typcial
# 	login response.
# 	"""
# 	
# 	session = UserSession.current()
# 	
# 	if not session or not session.validate():
# 		plus_error(401, "Session is not valid")
# 	
# 	user = session.get_user()
# 	
# 	return make_login_response(user, session)

# @bp.get("/<int:version>/<appname>/session")
# def session_get_status(version, appname):
# 	"""
# 	Get the status of the session for the given device and game.
# 	"""
# 	
# 	try:
# 		user = User.current()
# 		
# 		return {
# 			"success": True,
# 			"gamertag": user.gamertag,
# 			"badge_id": user.badge_id,
# 			"configuration": {},
# 			"messages": [
# 				{
# 					"title": "Katten Server",
# 					"text": "Welcome to Katten server!",
# 					"url": "https://example.com",
# 					"alert": True,
# 					"web_view": False,
# 				}
# 			]
# 		}
# 	except SessionError:
# 		plus_error(401, "Invalid session")
