#!/usr/bin/env python3
"""
Touch Pets main server

Everything is just going in one file here.
"""

from config import *
from database import *
import database

from flask import Flask, Response, Blueprint, request, g
import util
from pathlib import Path

import gamedata
import traceback

ERROR_NOT_AUTHENTICATED = "Not authenticated"
ERROR_WRONG_VERSION = "Wrong version"
ERROR_SERVER_UNAVAILABLE = "Server unavailable"
ERROR_INVALID_RECEIPT = "Invalid receipt"

class Property(Model):
	__tablename__ = "properties"
	
	type = Column(String(15), primary_key=True)
	objectID = Column(Integer, primary_key=True)
	categoryID = Column(Integer, primary_key=True)
	propertyID = Column(Integer, primary_key=True)
	value = Column(Integer, nullable=False)
	
	def __init__(self, type, objectID, categoryID, propertyID, value):
		self.type = type
		self.objectID = objectID
		self.categoryID = categoryID
		self.propertyID = propertyID
		self.value = value
	
	@classmethod
	def set(self, type, objectID, categoryID, propertyID, value):
		result = database.session.query(self).where(self.type == type.__name__, self.objectID == objectID, self.categoryID == categoryID, self.propertyID == propertyID).one_or_none()
		print(result)
		
		if not result:
			prop = self(type.__name__, objectID, categoryID, propertyID, value)
			database.add(prop)
		else:
			result.value = value
	
	@classmethod
	def delta(self, type, objectID, categoryID, propertyID, deltavalue):
		result = database.session.query(self).where(self.type == type.__name__, self.objectID == objectID, self.categoryID == categoryID, self.propertyID == propertyID).one_or_none()
		
		if not result:
			# We should probably never get here, but just in case this seems
			# like reasonable behaviour.
			prop = self(type.__name__, objectID, categoryID, propertyID, deltavalue)
			database.add(prop)
		else:
			result.value += deltavalue
	
	@classmethod
	def get_all(self, type, objectID):
		return database.session.query(self).where(self.type == type.__name__, self.objectID == objectID).all()
	
	@classmethod
	def get_all_as_xml_elements(self, type, objectID):
		props = []
		
		for prop in self.get_all(type, objectID):
			element = Element("property", {"category": str(prop.categoryID), "id": str(prop.propertyID)})
			element.text = str(prop.value)
			props.append(element)
		
		return props
	
	@classmethod
	def clear_all(self, type, objectID):
		"""Clear all properties from an object given its id. Most useful for
		resetting players/pets/etc when testing stuff."""
		
		for prop in self.get_all(type, objectID):
			database.delete(prop)

class Player:
	"""Mostly a nothing-class with a few utility methods. We keep user stuff to
	the Plus+ side mostly"""
	
	supports_properties = True
	
	def __init__(self, _d):
		self.__dict__ = _d
		self.username = self.gamertag
		self.playerID = self.user_id
		self.success = True
	
	def to_xml(self):
		root = Element(self.__class__.__name__.lower())
		
		for col in self.__dict__.keys():
			e = Element(col)
			e.text = str(getattr(self, col))
			root.append(e)
		
		for prop in Property.get_all_as_xml_elements(self.__class__, self.playerID):
			root.append(prop)
		
		for item in InventoryItem.for_player_as_xml(self.playerID):
			root.append(item)
		
		return root
	
	def assert_owned_by(self, playerID):
		assert(self.playerID == playerID)
	
	@classmethod
	def current(self):
		result = util.post(f"http://{TP_PLUS_SERVER}/1/{TP_APPNAME}/session", {"auth_token": request.form["sessionToken"]})
		
		if result["success"]:
			return self(result["profile"])
		else:
			raise NotAuthenticated("Not authenticated")
	
	@classmethod
	def get(self, id):
		result = util.get(f"http://{TP_PLUS_SERVER}/1/{TP_APPNAME}/users/{id}")
		
		if result["success"]:
			return self(result)
		else:
			raise NoResultFound()

class Pet(Model):
	__tablename__ = "pets"
	
	supports_properties = True
	
	petID = Column(Integer, primary_key=True)
	playerID = Column(Integer, nullable=False, index=True)
	ready = Column(Integer, nullable=False)
	gender = Column(Integer, nullable=False)
	timeadopted = Column(Integer, nullable=False)
	breedID = Column(Integer, nullable=False)
	petname = Column(String(50), nullable=False)
	
	def __init__(self, playerID, gender, breedID, petname):
		self.playerID = playerID
		self.ready = 0
		self.gender = gender
		self.timeadopted = util.time()
		self.breedID = breedID
		self.petname = petname
	
	def to_xml(self):
		root = super().to_xml()
		
		for prop in Property.get_all_as_xml_elements(self.__class__, self.petID):
			root.append(prop)
		
		return root
	
	@classmethod
	def add(self, player, args):
		kitty = self(player.playerID, int(args['gender']), int(args['breedID']), args['petname'])
		database.add(kitty)
		database.commit()
		return self.many_to_xml([kitty])
	
	@classmethod
	def for_player_as_xml(self, id):
		pets = self.for_player(id)
		return self.many_to_xml(pets)

class InventoryItem(Model):
	__tablename__ = "inventory_items"
	
	playerID = Column(Integer, primary_key=True)
	inventoryID = Column(Integer, primary_key=True)
	known = Column(Boolean, nullable=False)
	rewarded = Column(Boolean, nullable=False)
	gifted = Column(Boolean, nullable=False)
	owned = Column(Boolean, nullable=False)
	timeaccquired = Column(Integer, nullable=False)
	quantity = Column(Integer, nullable=False)
	decaystate = Column(Integer, nullable=False)
	frompetid = Column(Integer, ForeignKey("pets.petID"), nullable=False)
	topetid = Column(Integer, ForeignKey("pets.petID"), nullable=False)
	timegifted = Column(Integer, nullable=False)
	isnew = Column(Boolean, nullable=False)
	
	def __init__(self, playerID, inventoryID, known, rewarded, gifted, owned, quantity, frompetid, topetid, timegifted, isnew):
		self.playerID = playerID
		self.inventoryID = inventoryID
		self.known = known
		self.rewarded = rewarded
		self.gifted = gifted
		self.owned = owned
		self.timeaccquired = util.time()
		self.quantity = quantity
		self.decaystate = 0
		self.frompetid = frompetid
		self.topetid = topetid
		self.timegifted = timegifted
		self.isnew = isnew
	
	@classmethod
	def add(self, player, args):
		self.add_internal(
			player.playerID, 
			int(args['inventoryID']),
			int(args['known']),
			int(args['rewarded']),
			int(args['gifted']),
			int(args['owned']),
			# int(args['timeaccquired']),
			int(args['quantity']),
			int(args['fromdogID']),
			int(args['todogID']),
			int(args['timegifted']),
			bool(args['isnew']),
		)
		database.commit()
		return player.to_xml()
	
	@classmethod
	def add_internal(self, playerID, inventoryID, known, rewarded, gifted, owned, quantity, frompetid, topetid, timegifted, isnew):
		item = database.session.query(self).where(self.playerID == playerID, self.inventoryID == inventoryID).one_or_none()
		
		if item:
			item.quantity += 1 # TODO: Is this ok ??? no...
		else:
			item = self(playerID, inventoryID, known, rewarded, gifted, owned, quantity, frompetid, topetid, timegifted, isnew)
			database.add(item)
		
		return item
	
	@classmethod
	def decay(self, playerID, inventoryID, decay):
		item = database.session.query(self).where(self.playerID == playerID, self.inventoryID == inventoryID).one()
		item.decaystate += decay
	
	@classmethod
	def for_player_as_xml(self, playerID):
		items = []
		
		for item in self.for_player(playerID):
			attrs = {
				"inventoryID": item.inventoryID,
				"known": item.known,
				"rewarded": item.rewarded,
				"owned": item.owned,
				"gifted": item.gifted,
				"timeaccquired": item.timeaccquired,
				"quantity": item.quantity,
				"decaystate": item.decaystate,
				"fromdogID": item.frompetid,
				"todogID": item.topetid,
				"timegifted": item.timegifted,
				"isnew": item.isnew,
			}
			
			for key in attrs:
				attrs[key] = str(attrs[key]) if type(attrs[key]) != bool else str(int(attrs[key]))
			
			items.append(Element("inventory", attrs))
		
		return items

class Event(Model):
	__tablename__ = "events"
	
	# TODO!!! Add primarypetID and secondarypetID because I'm stupid and forgot
	# them!!!
	
	eventID = Column(Integer, primary_key=True)
	typeID = Column(Integer, nullable=False)
	primaryplayerID = Column(Integer, nullable=False, index=True)
	secondaryplayerID = Column(Integer, nullable=False, index=True)
	primaryvalue = Column(Integer, nullable=False)
	secondaryvalue = Column(Integer, nullable=False)
	created = Column(Integer, nullable=False)
	urlencoded_data = Column(String, nullable=False)
	isGlobal = Column(Boolean, nullable=False)
	
	def __init__(self, typeID, primaryplayerID, secondaryplayerID, primaryvalue, secondaryvalue, created, urlencoded_data, isGlobal=False):
		# self.eventID = eventID
		self.typeID = typeID
		self.primaryplayerID = primaryplayerID
		self.secondaryplayerID = secondaryplayerID
		self.primaryvalue = primaryvalue
		self.secondaryvalue = secondaryvalue
		self.created = created
		self.urlencoded_data = urlencoded_data
		self.isGlobal = isGlobal
	
	@classmethod
	def add(self, player, args):
		event = self(
			int(args['typeID']),
			int(args['primaryplayerID']),
			int(args['secondaryplayerID']),
			# int(args['primarypetID']), - when the fuck did these get lost??
			# int(args['secondarypetID']),
			int(args['primaryvalue']),
			int(args['secondaryvalue']),
			int(args['created']),
			args.get('urlencoded_data', ''), # TODO make mandatory when we know this is the name
		)
		database.add(event)
		database.commit()
		
		return event.to_xml()
	
	@classmethod
	def for_player(self, id):
		return database.session.query(self).where((self.primaryplayerID == id) | (self.secondaryplayerID == id)).all()

MODELS = {
	"player": Player,
	"pet": Pet,
	"inventory": InventoryItem,
	"event": Event,
}

database.create_tables()

class NotAuthenticated(Exception): pass

# def get_player_data(plus_profile, player_id):
# 	data = "<player>"
# 	
# 	data += f"<playerID>{player_id}</playerID>"
# 	data += f"<username>{plus_profile['gamertag']}</username>"
# 	
# 	for k, v in plus_profile.items():
# 		if k not in {"user_id"}:
# 			data += f"<{k}>{v}</{k}>"
# 	
# 	data += Player(int(player_id)).propertiesAsXML()
# 	
# 	for inv in Inventory.lookup_many({"playerID": player_id}):
# 		data += inv.feildsAsInlineXML()
# 	
# 	data += "</player>"
# 	return data
# 
# def get_player_pets(select_id):
# 	data = "<pets>"
# 	
# 	for pet in Pet.lookup_many({"playerID": select_id}):
# 		data += pet.toXMLWithProperties()
# 	
# 	return data + "</pets>"

def wrap_response(elems):
	if type(elems) not in {list, tuple}: elems = [elems]
	
	root = Element("results") # TODO: I'm not sure if this is how <results> works, but the game doesn't really care.
	servertime = Element("servertime")
	servertime.text = str(util.time())
	root.append(servertime)
	
	for elem in elems:
		root.append(elem)
	
	return xml_tostring(root, "unicode")

def response_xml(elems=(), commit=True):
	# if commit: database.commit()
	return Response(wrap_response(elems), content_type="text/xml")

app = Flask(__name__)
app.register_blueprint(gamedata.gamedata)

# ============================
#          Main Route
# ============================
# touchpet = Blueprint("touchpet", __name__)

@app.post("/touchpet/")
def touchpet_index():
	version = request.form["version"] # Always 1
	cmd = request.form["cmd"]
	playerId_untrusted = int(request.form["playerID"])
	
	player = Player.current()
	
	# Players are a bit different and not (yet) explicitly stored in the
	# touch pets database
	if cmd == "player":
		return response_xml(player.to_xml(), False)
	
	elif cmd == "pets":
		# print("Get pets")
		# return Response(finish_response(get_player_pets(int(request.form["selectID"]))), mimetype="text/xml")
		return response_xml(Pet.for_player_as_xml(int(request.form["selectID"])))
	
	elif cmd == "setpetready":
		# HACK see note in delta/set property
		if request.form["petID"] == '0':
			return response_xml(Pet.for_player_as_xml(player.playerID))
		
		pet = Pet.get(int(request.form["petID"]))
		pet.assert_owned_by(player.playerID)
		pet.ready = int(request.form["ready"])
		database.commit()
		return response_xml(pet.to_xml())
	
	elif cmd == "decayinventory":
# 		print("Decay inventory")
# 		item = Inventory.lookup({"playerID": playerId, "inventoryID": int(request.form["inventoryID"])})
# 		
# 		if (item):
# 			item.decay(request.form["decayamount"])
# 		
# 		return Response(finish_response(get_player_data(playerProfile, playerId)), mimetype="text/xml")
		InventoryItem.decay(player.playerID, int(request.form["inventoryID"]), int(request.form["decayamount"]))
		database.commit()
		return response_xml(player.to_xml())
	
	elif cmd == "clearfriends":
		# ???
		# return Response(finish_response(), mimetype="text/xml")
		return response_xml(player.to_xml())
	
# 	elif cmd == "setpetready":
# 		print("Set pet ready")
# 		pet = Pet.lookup({"_id": int(request.form["petID"])})
# 		pet.ready = int(request.form["ready"])
# 		pet.save()
# 		
# 		return Response(finish_response(pet.toXMLWithProperties()), mimetype="text/xml")
	
	elif cmd == "mega":
		# mega
		# return Response(finish_response('<mega count="0" totalcount="0" pluscount="0" followercount="0" totalpluscount="0" totalfollowercount="0"><friends><friend><username>knot2</username></friend></friends></mega>'), mimetype="text/xml")
		# TODO
		mega = Element("mega", {"count": "0", "totalcount": "0", "pluscount": "0", "followercount": "0", "totalpluscount": "0", "totalfollowercount": "0"})
		return response_xml(mega, False)
	
	elif cmd == "missionsmega":
		# TODO
		mega = Element("mega", {"count": "0", "totalcount": "0", "pluscount": "0", "followercount": "0", "totalpluscount": "0", "totalfollowercount": "0"})
		return response_xml(mega, False)
	
	elif cmd == "playerevents":
		# return Response(finish_response(Event.asXMLForAllMatching({"playerID": playerId})), mimetype="text/xml")
		return response_xml(Event.for_player_as_xml(player.playerID), False)
	
	elif cmd == "queuerecharge":
		# seems related to push notifications, which we can ignore and just send
		# back a player object (which is the acceptable class for this request)
		return response_xml(player.to_xml(), False)
	
	elif cmd == "cancelrecharge":
		# seems related to push notifications, which we can ignore and just send
		# back a player object (which is the acceptable class for this request)
		return response_xml(player.to_xml(), False)
	
	elif cmd.startswith("add"):
		# Generic handling of add command - it is expected that all classes
		# implement the add classmethod
		class_name = cmd.removeprefix("add")
		
		if class_name not in MODELS:
			raise Exception("Class name not in models!")
		
		data = MODELS[class_name].add(player, request.form)
		
		# IMPORTANT: Implementations of the add() method are REQUIRED to
		# commit to the database themselves!
		
		return response_xml(data)
		
# 		data = None
# 		
# 		if modelName == "inventory":
# 			models[modelName].addOrUpdate(request.form)
# 			data = get_player_data(playerProfile, playerId)
# 		else:
# 			obj = models[modelName].add(request.form)
# 			data = f"<{modelName}s>{obj.toXMLWithProperties()}</{modelName}s>"
# 		
# 		if modelName == "player":
# 			data = get_player_data(playerProfile, playerId)
# 		
# 		return Response(finish_response(data), mimetype="text/xml")
	
	elif cmd.startswith(('set', 'delta')) and cmd.endswith("property"):
		# Generic handling of property set and delta commands
		class_name = cmd.removeprefix("set").removeprefix("delta").removesuffix("property")
		should_delta = cmd.startswith('delta')
		
		# TODO Don't hardcode this, rely on Model.supports_properties instead
		if class_name not in {"pet", "player"}:
			raise Exception("Does not suppport properties!")
		
		# HACK because sometimes katten would send an invalid ID and fuck
		# everything up!
		if (request.form[f"{class_name}ID"] == '0'):
			# Invaild id, to prevent spamming return something valid looking
			return response_xml(MODELS[class_name].for_player_as_xml(player.playerID), False)
		
		model = MODELS[class_name].get(int(request.form[f"{class_name}ID"]))
		model.assert_owned_by(player.playerID)
		
		# Yes, this works.
		update_func = Property.delta if should_delta else Property.set
		
		# Set one
		if "propertyvalue" in request.form:
			update_func(
				MODELS[class_name],
				int(request.form[f"{class_name}ID"]),
				int(request.form["categoryID"]),
				int(request.form["propertyID"]),
				int(request.form["propertyvalue"])
			)
		# Set many
		else:
			index = 0
			
			while f"propertyvalue[{index}]" in request.form:
				update_func(
					MODELS[class_name],
					int(request.form[f"{class_name}ID"]),
					int(request.form[f"categoryID[{index}]"]),
					int(request.form[f"propertyID[{index}]"]),
					int(request.form[f"propertyvalue[{index}]"])
				)
				index += 1
		
		database.commit()
		
		return response_xml(model.to_xml(), False)
		
# 		print(f"Setting property for type {modelName}")
# 		obj = models[modelName](int(request.form[f"{modelName}ID"]))
# 		
# 		if "propertyvalue" in request.form:
# 			obj.setProperty(request.form["categoryID"], request.form["propertyID"], request.form["propertyvalue"])
# 		else:
# 			try:
# 				i = 0
# 				while True:
# 					obj.setProperty(request.form[f"categoryID[{i}]"], request.form[f"propertyID[{i}]"], request.form[f"propertyvalue[{i}]"])
# 					i += 1
# 			except KeyError:
# 				pass
# 		
# 		data = f"<{modelName}s>{obj.toXMLWithProperties()}</{modelName}s>"
# 		
# 		if modelName == "player":
# 			data = get_player_data(playerProfile, playerId)
# 		
# 		return Response(finish_response(data), mimetype="text/xml")
	
	# elif cmd.startswith("delta") and cmd.endswith("property"):
		# TODO DRY, again
# 		modelName = cmd[5:-8]
# 		print(f"Delta {modelName} property")
# 		obj = models[modelName](int(request.form[f"{modelName}ID"]))
# 		
# 		if "propertyvalue" in request.form:
# 			obj.deltaProperty(request.form["categoryID"], request.form["propertyID"], request.form["propertyvalue"])
# 		else:
# 			try:
# 				i = 0
# 				while True:
# 					obj.deltaProperty(request.form[f"categoryID[{i}]"], request.form[f"propertyID[{i}]"], request.form[f"propertyvalue[{i}]"])
# 					i += 1
# 			except KeyError:
# 				pass
# 		
# 		data = f"<{modelName}s>{obj.toXMLWithProperties()}</{modelName}s>"
# 		
# 		if modelName == "player":
# 			data = get_player_data(playerProfile, playerId)
# 		
# 		return Response(finish_response(data), mimetype="text/xml")
	
	else:
		# print(f'*** ERROR: Unknown command: {cmd}')
		return Response(ERROR_SERVER_UNAVAILABLE, mimetype="text/plain")

@app.get("/touchpet/debug_clear/<type_name>/<int:id>")
def debug_clear(type_name, id):
	Property.clear_all(MODELS[type_name], id)
	
	if request.args.get('delete', '0') == '1':
		database.delete(MODELS[type_name].get(id))
	
	database.commit()
	
	return Response("Debug clear properties success", 200)

@app.get("/touchpet/debug_deltacoins/<int:id>/<int:amount>")
def debug_deltacoins(id, amount):
	Property.delta(Player, id, 1, 3, amount)
	database.commit()
	return Response(f"Added {amount} coins to player id {id}", 200)

@app.errorhandler(Exception)
def touchpet_handle_errors(error):
	traceback.print_exception(error)
	return Response(ERROR_SERVER_UNAVAILABLE, 200, content_type="text/plain")

@app.errorhandler(NotAuthenticated)
def touchpet_handle_not_authed(error):
	return Response(ERROR_NOT_AUTHENTICATED, 200, content_type="text/plain")

@app.teardown_appcontext
def shutdown_database_session(exception=None):
    database.session.remove()

# app.register_blueprint(touchpet)

@app.get("/")
def index():
	return f"Katten Touch Pets server (running for {TP_APPNAME})"

# @app.before_request
# def configure_appname():
# 	"""
# 	Try to guess the appname from the user agent. Doing this allows us to use
# 	multiple apps (e.g. TPD, TPD2, TPC) with different data while running only
# 	one server.
# 	"""
# 	
# 	ua = [x.split('/') for x in request.user_agent.string.split()]
# 	
# 	for entry in ua:
# 		if entry[0] in TP_DATABASE_MAPS:
# 			g.appname = entry[0]
# 			break
# 	else:
# 		g.appname = TP_DEFAULT_APPNAME

# Misc todos:
# - should really store uuid's and check against them so we don't end up in a
# situation where we process an event twice
