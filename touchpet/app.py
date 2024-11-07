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
		self.type = "Object"
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
	
	@classmethod
	def delta(self, typeName, objectId, categoryId, propertyId, amount):
		prop = self.lookup({"type": typeName, "object_id": objectId, "category_id": categoryId, "property_id": propertyId})
		
		# For now, just create it as zero
		if not prop:
			self.set(typeName, objectId, categoryId, propertyId, amount)
			return
		
		prop.value += int(amount)
		prop.save()

class Model(Persistent):
	"""
	Implements a more structured model for most things in TPC
	"""
	
	special_id = False
	
	def on_init(self):
		struct = self.__class__.struct
		
		for feildname, feildtype in struct.items():
			setattr(self, feildname, feildtype())
	
	def on_load(self):
		struct = self.__class__.struct
		
		# Check for new or updated feilds
		for feildname, feildtype in struct.items():
			if hasattr(self, feildname):
				if (type(getattr(self, feildname)) != feildtype):
					setattr(self, feildname, feildtype())
			else:
				setattr(self, feildname, feildtype())
		
		# Delete unused feilds
		for feildname, feildvalue in self.__dict__.items():
			if not feildname.startswith("_") and feildname not in struct:
				delattr(self, feildname)
	
	@classmethod
	def loadFromValues(self, obj, values):
		"""
		Load values into this object
		"""
		
		for key, value in values.items():
			if (key in self.struct):
				setattr(obj, key, self.struct[key](value))
	
	@classmethod
	def add(self, initialValues):
		"""
		Add a new object of this type with initialValues
		"""
		
		obj = self()
		self.loadFromValues(obj, initialValues)
		obj.save()
		
		return obj
	
	@classmethod
	def asXMLForAllMatching(self, filter):
		lower = self.__name__.lower()
		xml = f"<{lower}s>"
		objs = self.lookup_many(filter)
		
		for obj in objs:
			xml += obj.toXMLWithProperties()
		
		return xml + f"</{lower}s>"
	
	def setProperty(self, catid, propid, value):
		Property.set(self.__class__.__name__, self._id, int(catid), int(propid), int(value))
	
	def deltaProperty(self, catid, propid, value):
		Property.delta(self.__class__.__name__, self._id, int(catid), int(propid), int(value))
	
	def feildsAsXML(self):
		# For <feild1>value1</feild1><feild2>value2</feild2>...
		lower = self.__class__.__name__.lower()
		xml = f"<{lower}ID>{self._id}</{lower}ID>" if self.__class__.special_id else ""
		
		for key, value in self.__dict__.items():
			if not key.startswith("_"):
				xml += f"<{key}>{value}</{key}>"
		
		return xml
	
	def feildsAsInlineXML(self):
		# For <classname feild1="value1" feild2="value2" />
		lower = self.__class__.__name__.lower()
		xml = [f'{lower}ID="{self._id}"'] if self.__class__.special_id else []
		
		for key, value in self.__dict__.items():
			if not key.startswith("_"):
				xml.append(f'{key}="{value}"')
		
		return f"<{lower} " + " ".join(xml) + "/>"
	
	def propertiesAsXML(self):
		data = ""
		
		for prop in Property.getAll(self.__class__.__name__, self._id):
			data += f'<property category="{prop.category_id}" id="{prop.property_id}">{prop.value}</property>'
		
		return data
	
	def toXMLWithProperties(self):
		lower = self.__class__.__name__.lower()
		
		return f"<{lower}>{self.propertiesAsXML()}{self.feildsAsXML()}</{lower}>"

class Player(Model):
	struct = {}

class Inventory(Model):
	struct = {
		"inventoryID": int,
		"known": int,
		"rewarded": int,
		"owned": int,
		"gifted": int,
		"quantity": int,
		"decaystate": int,
		"fromdogID": int,
		"todogID": int,
		"timegifted": int,
		"isnew": int,
		"playerID": int,
	}
	
	@classmethod
	def addOrUpdate(self, newValues):
		inv = self.lookup({"inventoryID": int(newValues["inventoryID"]), "playerID": int(newValues["playerID"])})
		
		if inv:
			inv.__class__.loadFromValues(inv, newValues)
			inv.save()
		else:
			self.add(newValues)
	
	def decay(self, amount):
		self.decaystate += int(amount)
		self.save()

class Pet(Model):
	struct = {
		"petname": str,
		"breedID": int,
		"gender": int,
		"ready": int,
		"playerID": int,
	}
	special_id = True

class Event(Model):
	struct = {
		"typeID": int,
		"created": int,
		"primarypetID": int,
		"primaryplayerID": int,
		"primaryvalue": int,
		"secondarypetID": int,
		"secondaryplayerID": int,
		"secondaryvalue": int,
		"urlencoded_data": str,
	}
	special_id = True

models = {
	"player": Player,
	"inventory": Inventory,
	"pet": Pet,
	"event": Event,
}

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

def get_player_data(plus_profile, player_id):
	data = "<player>"
	
	data += f"<playerID>{player_id}</playerID>"
	data += f"<username>{plus_profile['gamertag']}</username>"
	
	data += Player(int(player_id)).propertiesAsXML()
	
	for inv in Inventory.lookup_many({"playerID": player_id}):
		data += inv.feildsAsInlineXML()
	
	data += "</player>"
	return data

def get_player_pets(select_id):
	data = "<pets>"
	
	for pet in Pet.lookup_many({"playerID": select_id}):
		data += pet.toXMLWithProperties()
	
	return data + "</pets>"

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
	
	# Players are a bit different and not (yet) explicitly stored in the
	# touch pets database
	if cmd == "player":
		return Response(finish_response(get_player_data(playerProfile, playerId)), mimetype="text/xml")
	
	elif cmd == "decayinventory":
		print("Decay inventory")
		item = Inventory.lookup({"playerID": playerId, "inventoryID": int(request.form["inventoryID"])})
		
		if (item):
			item.decay(request.form["decayamount"])
		
		return Response(finish_response(get_player_data(playerProfile, playerId)), mimetype="text/xml")
	
	elif cmd == "clearfriends":
		# ???
		return Response(finish_response(), mimetype="text/xml")
	
	elif cmd == "pets":
		# for testing
		# return Response(finish_response("<pets><pet><petID>5</petID><petname>Jens</petname></pet></pets>"), mimetype="text/xml")
		print("Get pets")
		return Response(finish_response(get_player_pets(int(request.form["selectID"]))), mimetype="text/xml")
	
	elif cmd == "setpetready":
		print("Set pet ready")
		pet = Pet.lookup({"_id": int(request.form["petID"])})
		pet.ready = int(request.form["ready"])
		pet.save()
		
		return Response(finish_response(pet.toXMLWithProperties()), mimetype="text/xml")
	
	elif cmd == "mega":
		# mega
		return Response(finish_response('<mega count="0" totalcount="0" pluscount="0" followercount="0" totalpluscount="0" totalfollowercount="0"><friends><friend><username>knot2</username></friend></friends></mega>'), mimetype="text/xml")
	
	elif cmd == "missionsmega":
		return Response(finish_response(), mimetype="text/xml")
	
	elif cmd == "playerevents":
		# HACK: We probably need to consider the primaryplayerID and
		# secondaryplayerID
		return Response(finish_response(Event.asXMLForAllMatching({"playerID": playerId})), mimetype="text/xml")
	
	elif cmd.startswith("add"):
		modelName = cmd[3:]
		print(f"Adding item of type {modelName}")
		
		data = None
		
		if modelName == "inventory":
			models[modelName].addOrUpdate(request.form)
			data = get_player_data(playerProfile, playerId)
		else:
			obj = models[modelName].add(request.form)
			data = f"<{modelName}s>{obj.toXMLWithProperties()}</{modelName}s>"
		
		return Response(finish_response(data), mimetype="text/xml")
	
	elif cmd.startswith("set") and cmd.endswith("property"):
		modelName = cmd[3:-8]
		print(f"Setting property for type {modelName}")
		obj = models[modelName](int(request.form[f"{modelName}ID"]))
		
		if "propertyvalue" in request.form:
			obj.setProperty(request.form["categoryID"], request.form["propertyID"], request.form["propertyvalue"])
		else:
			try:
				i = 0
				while True:
					obj.setProperty(request.form[f"categoryID[{i}]"], request.form[f"propertyID[{i}]"], request.form[f"propertyvalue[{i}]"])
					i += 1
			except KeyError:
				pass
		
		data = f"<{modelName}s>{obj.toXMLWithProperties()}</{modelName}s>"
		
		return Response(finish_response(data), mimetype="text/xml")
	
	elif cmd.startswith("delta") and cmd.endswith("property"):
		# TODO DRY, again
		modelName = cmd[5:-8]
		print(f"Delta {modelName} property")
		obj = models[modelName](int(request.form[f"{modelName}ID"]))
		
		if "propertyvalue" in request.form:
			obj.deltaProperty(request.form["categoryID"], request.form["propertyID"], request.form["propertyvalue"])
		else:
			try:
				i = 0
				while True:
					obj.deltaProperty(request.form[f"categoryID[{i}]"], request.form[f"propertyID[{i}]"], request.form[f"propertyvalue[{i}]"])
					i += 1
			except KeyError:
				pass
		
		data = f"<{modelName}s>{obj.toXMLWithProperties()}</{modelName}s>"
		
		return Response(finish_response(data), mimetype="text/xml")
	
	else:
		print(f'*** unknown cmd: {cmd} ***')
		return Response(ERROR_SERVER_UNAVAILABLE, mimetype="text/xml")

@app.get("/")
def index():
	return "Katten Touch Pets server"

# Misc todos:
# - should really store uuid's and check against them so we don't end up in a
# situation where we process an event twice
