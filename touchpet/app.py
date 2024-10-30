from flask import Flask, Response, request
from config import *
import util
from persist import Persistent

ERROR_NOT_AUTHENTICATED = "Not authenticated"
ERROR_WRONG_VERSION = "Wrong version"
ERROR_SERVER_UNAVAILABLE = "Server unavailable"
ERROR_INVALID_RECEIPT = "Invalid receipt"

class Property(Persistent):
	"""
	A property for any type of object
	"""
	
	version = 1
	
	def on_init(self):
		self.type = "object"
		self.object_id = 0
		self.category_id = 0
		self.property_id = 0
		self.value = 0
	
	@classmethod
	def get(self, typeName, objectId, categoryId, propertyId):
		prop = self.lookup({"type": typeName, "object_id": objectId, "category_id": categoryId, "property_id": propertyId})
		return self.value
	
	@classmethod
	def getAll(self, typeName, objectId):
		return self.lookup_many({"type": typeName, "object_id": objectId})
	
	@classmethod
	def set(self, typeName, objectId, categoryId, propertyId, value):
		prop = self.lookup({"type": typeName, "object_id": objectId, "category_id": categoryId, "property_id": propertyId})
		
		if not prop:
			prop = self()
		
		prop.type = typeName
		prop.object_id = objectId
		prop.category_id = categoryId
		prop.property_id = propertyId
		prop.value = int(value)
		prop.save()

app = Flask(__name__)

@app.get("/touchpet/gamedata/get_dlc.php")
def get_dlc_php():
	return ""

@app.get("/touchpet/gamedata/messages.php")
def messages_php():
	return ""

@app.get("/touchpet/gamedata/rewards.php")
def rewards_php():
	return ""

@app.get("/touchpet/gamedata/getpid.php")
def getpid_php():
	return ""

@app.get("/touchpet/gamedata/petmaster.php")
def petmaster_php():
	return "Katten does not support microtransactions."

def validate_session(token, player_id):
	result = util.post(f"http://{PLUS_SERVER}/1/{TP_APPNAME}/session", {"auth_token": token})
	return result["profile"] if result["success"] else None

def get_player_data(player_id):
	data = f"<player><playerID>{player_id}</playerID>"
	
	for prop in Property.getAll("player", player_id):
		data += f'<property category="{prop.category_id}" id="{prop.property_id}">{prop.value}</property>'
	
	data += "</player>"
	return data

def make_friend_from_profile(profile):
	s = "<friend>"
	
	for k, v in profile.items():
		s += f"<{k}>{v}</{k}>"
	
	return s + "</friend>"

def finish_response(data=""):
	return f"<results><servertime>{util.time()}</servertime>{data}</results>"

@app.post("/touchpet/")
def touchpet_index():
	version = request.form["version"] # Always 1
	cmd = request.form["cmd"]
	playerId = int(request.form["playerID"])
	sessionToken = request.form["sessionToken"]
	
	playerProfile = validate_session(sessionToken, playerId)
	if (not playerProfile):
		return ERROR_NOT_AUTHENTICATED
	
	match cmd:
		case "player":
			return Response(finish_response(get_player_data(playerId)), mimetype="text/xml")
		
		case "setplayerproperty":
			categoryId = int(request.form["categoryID"])
			propertyId = int(request.form["propertyID"])
			Property.set("player", playerId, categoryId, propertyId, int(request.form["propertyvalue"]))
			# return Response(finish_response(get_player_data(playerId)), mimetype="text/xml")
			return Response(finish_response(), mimetype="text/xml")
		
		case "clearfriends":
			# ???
			return Response(finish_response(), mimetype="text/xml")
		
		case "pets":
			# for testing
			return Response(finish_response("<pets><pet><petname>Jens</petname></pet></pets>"), mimetype="text/xml")
		
		case "mega":
			# mega
			return Response(finish_response('<mega count="0" totalcount="0" pluscount="0" followercount="0" totalpluscount="0" totalfollowercount="0"><friends></friends></mega>'), mimetype="text/xml")
		
		case "missionsmega":
			return Response(finish_response(), mimetype="text/xml")
		
		case "playerevents":
			return Response(finish_response(), mimetype="text/xml")
		
		case _:
			return Response(ERROR_SERVER_UNAVAILABLE, mimetype="text/xml")
