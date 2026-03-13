"""
Login sessions and security
"""

from config import *
from utils import *
import database
import secrets
from database import Model, Column, String, Integer, Boolean, ForeignKey, relationship
from flask import Blueprint, request
from game import Game

class InvalidSession(Exception):
	pass

class Session(Model):
	__tablename__ = "sessions"
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	token = Column(String, nullable=False, unique=True)
	login_time = Column(Integer, nullable=False)
	extra_data = Column(String, nullable=False)
	
	user = relationship("User", back_populates="sessions")
	
	def __init__(self, user):
		self.user = user
		self.token = secrets.token_hex(PLUS_SESSION_TOKEN_BITS >> 3).upper()
		self.login_time = unixtime()
		self.extra_data = ""
	
	@classmethod
	def current(self, do_plus_error=True):
		try:
			token = request.authorization.get("oauth_token", None)
			session = database.find_one(self, "token", token)
			return session
		except:
			if do_plus_error:
				plus_error(401, "Invalid session")
			else:
				raise InvalidSession("Invalid session")
	
	@classmethod
	def find(self, token):
		return database.find_one(self, "token", token)

bp = Blueprint(__name__, __name__)

@bp.get("/<int:version>/<appname>/session")
def session_get_status(version, appname):
	"""
	Get the status of the session for the given device and game.
	"""
	
	from system_message import SystemMessage
	
	try:
		session = Session.current()
		
		app = Game.find(appname)
		
		# its not broken anymore :D
		if app not in session.user.games:
			session.user.games.append(app)
			database.commit()
		
		return {
			"success": True,
			"gamertag": session.user.gamertag,
			"badge_id": session.user.badge_id,
			"configuration": {},
			"messages": SystemMessage.current_messages(),
			# "messages": [
			# 	{
			# 		"title": "Katten Server",
			# 		"text": "Welcome to Katten server!",
			# 		"url": "https://example.com",
			# 		"alert": True,
			# 		"web_view": False,
			# 	}
			# ]
		}
	except InvalidSession as e:
		plus_error(401, "Invalid session")

@bp.put("/<int:version>/<appname>/session")
def put_device_token(version, appname):
	# Not really important to do anything given we don't re-implement
	# notifications.
	return {
		"success": True,
	}

@bp.delete("/<int:version>/<appname>/session")
def delete_session(version, appname):
	session = Session.current()
	database.delete(session)
	database.commit()
	
	return {
		"success": True,
	}
