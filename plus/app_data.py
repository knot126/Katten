from utils import *

from base64 import b64encode, b64decode
import database
from game import Game
from user import User
from database import Model, Column, String, Integer, ForeignKey, relationship, NoResultFound
from flask import Blueprint, Response, request
import traceback

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
		return database.session.query(self).where(self.game == game, self.user == user, self.key == key).one()
	
	@classmethod
	def set(self, user, game, key, value, privacy):
		try:
			datum = self.get(user, game, key)
			datum.value = value
			datum.privacy = privacy
		except NoResultFound:
			database.add(self(user, game, key, value, privacy))
	
	@classmethod
	def all(self, user, game):
		return database.session.query(self).where(self.game == game, self.user == user).all()

bp = Blueprint(__name__, __name__)

@bp.post("/<int:version>/<appname>/users/<int:user_id>/user_data")
def user_data_set(version, appname, user_id):
	"""
	Save a key-value pair; ignores user id for now as it's not possbile to
	change someone else's user data.
	"""
	
	user = User.current()
	game = Game.find(appname)
	data = request.form.to_dict()
	
	if user.id != user_id:
		plus_error(400, "Cannot modify someone else's user data")
	
	# UserAppDataEntry.set(appname, user.get_id(), data["key"], data["privacy"], request.files["value"].read())
	Datum.set(user, game, data["key"], b64encode(request.files["value"].read()), data["privacy"])
	database.commit()
	
	return {
		"success": True
	}

@bp.get("/<int:version>/<appname>/users/<int:user_id>/user_data/<key>")
def user_data_get_one(version, appname, user_id, key):
	"""
	Get a single value from user data storage
	"""
	
	cur_user = User.current()
	user = User.get(user_id)
	game = Game.find(appname)
	
	# data = UserAppDataEntry.get(appname, user.get_id(), key)
	try:
		dat = Datum.get(user, game, key)
		
		if ((dat.privacy == 0 and user.id != cur_user.id) or (dat.privacy == 1 and not (user.is_friends_with(cur_user) or user.id == cur_user.id))):
			return plus_error(401, "You don't have permission to view this user data")
		
		return Response(b64decode(dat.value), mimetype='application/octet-stream')
	except Exception as e:
		traceback.print_exc()
		plus_error(404, "Key does not exist for user")

@bp.get("/<int:version>/<appname>/users/<int:user_id>/user_data")
def user_data_get_keys(version, appname, user_id):
	"""
	Get a list of keys that are stored for the given user
	TODO: Support for getting non-private keys of other users
	"""
	
	user = User.current()
	game = Game.find(appname)
	
	if user.id != user_id:
		plus_error(401, "You don't have permission to list keys from other users")
	
	# datas = []
	
	# for entry in UserAppDataEntry.lookup_many({"game": appname, "user": user.get_id()}):
		# datas.append(entry.key)
	
	return {
		"success": True,
		"datas": [datum.key for datum in Datum.all(user, game)],
		# "datas": datas,
	}
