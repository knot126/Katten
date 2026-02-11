"""
Login sessions and security
"""

from config import *
from utils import *
# from persist import Persistent
import database
import secrets
from database import Model, Column, String, Integer, Boolean, ForeignKey, relationship
from flask import Blueprint, request

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
	def current(self):
		try:
			token = request.authorization.get("oauth_token", None)
			session = database.find(self, "token", token)[0]
			return session
		except:
			raise InvalidSession("Invalid session")

bp = Blueprint(__name__, __name__)

@bp.get("/<int:version>/<appname>/session")
def session_get_status(version, appname):
	"""
	Get the status of the session for the given device and game.
	"""
	
	from system_messages import SystemMessage
	
	try:
		session = Session.current()
		
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
	except SessionError:
		plus_error(401, "Invalid session")

@bp.put("/<int:version>/<appname>/session")
def put_device_token(version, appname):
	# Not really important to do anything given we don't re-implement
	# notifications.
	return {
		"success": True,
	}

