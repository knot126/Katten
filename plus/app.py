from flask import Flask, request, make_response, url_for

app = Flask(__name__)

# Identification page
@app.route("/")
def index():
	return "<p><i>Katten Plus+ server</i></p>"

# Hack to make touch pets games happy
@app.get("/touchpet/gamedata/get_dlc.php")
def touchpet_gamedata_getdlc_hack():
	return ""

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
	print(request.form)
	
	return {}

@app.post("/<int:version>/<appname>/users/validate")
def users_validate(version, appname):
	"""
	Validate if a user's name, email, etc are valid
	"""
	
	return {
		"success": True,
	}
