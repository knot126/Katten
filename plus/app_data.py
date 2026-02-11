import database
from game import Game
from user import User
from database import Model, Column, String, Integer, ForeignKey, relationship
from flask import Blueprint, request

class Datum(Model):
	__tablename__ = "datums"
	
	id = Column(Integer, primary_key=True)
	game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	key = Column(String, nullable=False)
	value = Column(String, nullable=False)
	privacy = Column(Integer, nullable=False)
	
	game = relationship(Game)
	user = relationship(User, back_populates="datums")
	
	def __init__(self, user, game, key, value, privacy):
		self.user = user
		self.game = game
		self.key = key
		self.value = value
		self.privacy = privacy
	
	@classmethod
	def get(self, user, game, key):
		pass
	
	@classmethod
	def set(self, user, game, key, value, privacy):
		pass
	
	@classmethod
	def keys(self, user, game):
		pass

bp = Blueprint(__name__, __name__)

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
