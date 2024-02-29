from flask import Flask, request, make_response

app = Flask(__name__)

# Bogus snowflake implementation for now
_SNOWFLAKE_COUNTER = 0

def snowflake():
	global _SNOWFLAKE_COUNTER
	
	_SNOWFLAKE_COUNTER = (_SNOWFLAKE_COUNTER + 1) & 0xFFF
	
	import time
	
	return ((int(time.time() * 1000) - 1709164800000) << 22) | _SNOWFLAKE_COUNTER

@app.route("/_test/snowflakes/<int:count>")
def test_snowflakes(count):
	out = ""
	
	for i in range(count):
		sf = snowflake()
		out += f"{hex(sf)} {sf}<br/>"
	
	return out

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
