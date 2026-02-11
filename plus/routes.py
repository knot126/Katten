from flask import Blueprint, Response, request, g, make_response, url_for, abort, redirect
from user import *
from utils import *

bp = Blueprint(__name__, __name__)

# Identification page
@bp.route("/")
def index():
	return "<p><i>Katten Plus+ server</i></p>"

# Ping
@bp.get("/<int:version>/<appname>/ping")
def ping(version, appname):
	return make_response({
		"success": True,
	})

# Games
def list_games(appname):
	return {
		"success": True,
		"games": [
			{
				"app_key": appname,
				"name": appname,
				"publisher": "Katten Server",
				"category": "unknown",
				"featured": False,
				"leaderboards_count": 0,
				"achievements_count": 0,
				"id": 1,
				"master_product_id": 1,
				"icon_url": f"http://{request.host}/static/badges/0.png",
				"app_store_url": "http://example.com/",
				"feed_url": "http://example.com/",
				"catalog_url": "http://example.com/",
				"description": "This is the current game.",
				"phone_screenshot_urls": [f"http://{request.host}/static/badges/0.png"],
				"phone_thumbnail_urls": [f"http://{request.host}/static/badges/0.png"],
				"promotion_image_url": f"http://{request.host}/static/badges/0.png",
			}
		],
	}

@bp.get("/<int:version>/<appname>/games")
def get_games(version, appname):
	return list_games(appname)

@bp.get("/<int:version>/<appname>/users/<int:user_id>/games")
def get_user_games(version, appname, user_id):
	return list_games(appname)

# Users

@bp.put("/<int:version>/<appname>/users/<int:user_id>")
def users_update(version, appname, user_id):
	user = User.current()
	
	user_info = request.form.to_dict()
	
	user.set_motto(user_info.get("motto", ""))
	user.set_phone_number(user_info.get("phone_number", ""))
	user.set_badge_url(user_info.get("badge_id", ""))
	user.set_real_name(user_info.get("first_name", ""), user_info.get("last_name", ""))
	user.set_email(user_info.get("email", ""))
	user.set_fullname_privacy(user_info.get("fullname_privacy", 0))
	
	if ("password" in user_info and "password_confirmation" in user_info):
		if (user_info['password'] == user_info['password_confirmation']):
			try:
				user.set_password(user_info["password"])
			except ValidationError:
				plus_error(1, "Password is too short")
		else:
			plus_error(1, "Passwords do not match")
	
	user.save()
	
	return {"success": True}

@bp.get("/<int:version>/<appname>/users/<gamertag>")
def users_lookup_by_gamertag(version, appname, gamertag):
	user = User.lookup({"gamertag": gamertag})
	
	if not user:
		plus_error(404, "Playername not found!")
	
	result = user.to_dict()
	result["success"] = True
	return result

@bp.get("/<int:version>/<appname>/users/search")
def users_search(version, appname):
	criteria = None
	
	if "email_hash" in request.args:
		criteria = {"email_hash": request.args['email_hash']}
	
	users = User.lookup_many(criteria)
	
	return {"success": True, "list": [u.to_dict() for u in users]}

@bp.post("/<int:version>/<appname>/users/validate")
def users_validate(version, appname):
	"""
	Validate if a user's name, email, etc are valid
	"""
	
	field = request.form["field"]
	value = request.form["value"]
	
	msg = "Unknown field"
	
	match field:
		case "gamertag":
			msg = None if validate_gamertag(value) else "Invalid gamertag"
			if not msg:
				msg = None if User.lookup({"gamertag": value}) == None else "Gamertag already taken"
		case "password":
			msg = None if validate_password(value) else "Invalid password"
		case "email":
			msg = None if validate_email(value) else "Not a valid email"
		case "first_name" | "last_name":
			msg = None if validate_first_or_last(value) else f"Invalid {field.replace('_', ' ')}"
	
	return {"success": True} if not msg else {"success": False, "error": 1, "error_msg": msg}

@bp.post("/<int:version>/<appname>/users/<int:user_id>/user_data")
def user_data_set(version, appname, user_id):
	"""
	Save a key-value pair; ignores user id for now as it's not possbile to
	change someone else's user data atm.
	"""
	
	user = User.current()
	data = request.form.to_dict()
	
	UserAppDataEntry.set(appname, user.get_id(), data["key"], data["privacy"], request.files["value"].read())
	
	return {
		"success": True
	}

@bp.get("/<int:version>/<appname>/users/<int:user_id>/user_data/<key>")
def user_data_get_one(version, appname, user_id, key):
	"""
	Get a single value from user data storage
	"""
	
	user = User.current()
	data = UserAppDataEntry.get(appname, user.get_id(), key)
	
	return Response(data, mimetype='application/octet-stream')

@bp.get("/<int:version>/<appname>/users/<int:user_id>/user_data")
def user_data_get_keys(version, appname, user_id):
	"""
	Get a list of keys that are stored for the given user
	"""
	
	user = User.current()
	
	datas = []
	
	for entry in UserAppDataEntry.lookup_many({"game": appname, "user": user.get_id()}):
		datas.append(entry.key)
	
	return {
		"success": True,
		"datas": datas,
	}

@bp.get("/<int:version>/<appname>/user_updates")
def get_user_updates(version, appname):
	user = User.current()
	
	return {
		"success": True,
		"online_friends": [],
		"updates": [],
		"update_interval": PLUS_USER_UPDATE_INTERVAL,
	}

@bp.get("/<int:version>/<appname>/users/<int:user_id>/buddies")
def users_buddies(version, appname, user_id):
	user = User.current()
	
	return {
		"success": True,
		"list": [],
		"offset": 0,
		"total": 0,
	}

@bp.post("/<int:version>/<appname>/session")
def session_init(version, appname):
	# Katten doesn't really care about OAuth 1.0's signing things; it's only
	# relevant over an insecure HTTP connection anyway.
	
	# If there is an auth_token instead of gamertag and password then we're
	# logging in using an existing session.
	if "auth_token" in request.form:
		session = UserSession.lookup({"token": request.form["auth_token"]})
		
		if not session or not session.validate():
			plus_error(401, "Session is not valid")
		
		user = session.get_user()
		
		return make_login_response(user, session)
	else:
		try:
			result = User.login(request.form["gamertag"], request.form["password"])
			
			return make_login_response(result.user, result.session)
		except LoginError:
			plus_error(1, "Wrong username or password")

@bp.post("/<int:version>/<appname>/oauth/authorize_new")
def oauth_authorize_new(version, appname):
	"""
	This should do something oauth related but we can just return the typcial
	login response.
	"""
	
	session = UserSession.current()
	
	if not session or not session.validate():
		plus_error(401, "Session is not valid")
	
	user = session.get_user()
	
	return make_login_response(user, session)

@bp.get("/<int:version>/<appname>/session")
def session_get_status(version, appname):
	"""
	Get the status of the session for the given device and game.
	"""
	
	try:
		user = User.current()
		
		return {
			"success": True,
			"gamertag": user.gamertag,
			"badge_id": user.badge_id,
			"configuration": {},
			"messages": [
				{
					"title": "Katten Server",
					"text": "Welcome to Katten server!",
					"url": "https://example.com",
					"alert": True,
					"web_view": False,
				}
			]
		}
	except SessionError:
		plus_error(401, "Invalid session")
