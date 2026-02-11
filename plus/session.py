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

@bp.put("/<int:version>/<appname>/session")
def put_device_token(version, appname):
	# Not really important to do anything given we don't re-implement
	# notifications.
	return {
		"success": True,
	}
