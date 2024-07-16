# Identification page
@app.route("/")
def index():
	return "<p><i>Katten Plus+ server</i></p>"

# Ping
@app.get("/<int:version>/<appname>/ping")
def ping(version, appname):
	return make_response({
		"error": 0,
	})

# Games
@app.get("/<int:version>/<appname>/games")
def get_games(version, appname):
	return {
		"error": 0,
		"games": [],
	}

# Badges
@app.get("/<int:version>/<appname>/badges")
def badges(version, appname):
	return {
		"error": 0,
		"list": [
			{
				"name": "General",
				"badges": [
					{ "icon_url": f"http://{request.host}" + url_for("static", filename = "0.png") },
					{ "icon_url": f"http://{request.host}" + url_for("static", filename = "1.png") },
				],
			}
		],
	}

# Users
@app.post("/<int:version>/<appname>/users")
def users_register(version, appname):
	form_dict = request.form.to_dict()
	user_info = {}
	
	for k in form_dict:
		if k.startswith("user["):
			user_info[k[5:-1]] = form_dict[k]
	
	result = User.register(user_info)
	
	return make_login_response(result.user, result.session)
	# return {
	# 	"error_msg": "User creation not supported"
	# }

@app.post("/<int:version>/<appname>/users/validate")
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
	
	return {} if not msg else {"error_msg": msg}

@app.post("/<int:version>/<appname>/users/<int:uid>/user_data")
def user_data(version, appname, uid):
	return {
		"error": 1,
	}

@app.post("/<int:version>/<appname>/session")
def session_init(version, appname):
	# Katten doesn't really care about OAuth 1.0's signing things; it's only
	# relevant over an insecure HTTP connection anyway.
	
	return {
		"error_msg": "Login not supported yet!"
	}
	
	# return {
	# 	"success": False,
	# 	"auth_token": "totally_real_auth_token",
	# 	"oauth_token": "TokenXthatsXsentXtoXserverXsoXitXneverXseesXaccountXpw",
	# 	"oauth_secret": "totally_real_oauth_secret",
	# 	"user_id": 1,
	# }
