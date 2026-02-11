from flask import Blueprint, request

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
