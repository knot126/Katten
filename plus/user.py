"""
Account and user related stuff
"""

from config import *
# from persist import Persistent
import database
from database import NoResultFound, Model, Column, String, Integer, Boolean, ForeignKey, relationship
from asset import Asset, upload
from utils import *
from flask import Blueprint, request
import time
import password
import secrets
import re
import base64
import hashlib

import game
import asset

from session import Session
from game import Game

def validate_gamertag(gamertag):
	return re.match(r"[a-zA-Z0-9]{" + str(PLUS_GAMERTAG_MIN_LENGTH) + "," + str(PLUS_GAMERTAG_MAX_LENGTH) + r"}", gamertag) != None

def validate_password(password):
	return len(password) >= PLUS_PASSWORD_MIN_LENGTH

def validate_email(email):
	# Note: This only validates a subset of emails, to keep things simple.
	return re.match(r"^[a-zA-Z0-9\_\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\.\-]+$", email) != None

def validate_first_or_last(first_or_last):
	return re.match(r"^[A-Z][a-z]*$", first_or_last) != None

class ValidationError(Exception): pass # General error validating some data
class UserExistsError(Exception): pass # User with a gamertag already exists
class PasswordsDoNotMatchError(Exception): pass # Passwords don't match
class EmailUsedError(Exception): pass # The email is already used by someone else
class LoginError(Exception): pass # Errors while logging in
class SessionError(Exception): pass # When a session does not exist

# UserAndSession = namedtuple("UserAndSession", "user session")

class User(Model):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	gamertag = Column(String(PLUS_GAMERTAG_MAX_LENGTH), nullable=False, unique=True)
	score = Column(Integer, nullable=False)
	level = Column(Integer, nullable=False)
	badge_id = Column(Integer, nullable=False)
	photo_id = Column(Integer, ForeignKey("assets.id"))
	motto = Column(String)
	email = Column(String, nullable=False, unique=True)
	email_hash = Column(String, nullable=False)
	phone_number = Column(String)
	password = Column(String, nullable=False)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=False)
	opt_in = Column(Boolean, nullable=False)
	fullname_privacy = Column(Boolean, nullable=False)
	age_restricted = Column(Boolean, nullable=False)
	
	games = relationship("Game", secondary=game.user_games, back_populates="players")
	
	def __init__(self, gamertag, password, email, badge_id, first_name="", last_name="", age_restricted=False, opt_in=False):
		self.set_gamertag(gamertag)
		self.set_password(password)
		self.set_email(email)
		self.score = 0
		self.level = 0
		self.badge_id = badge_id
		self.photo_id = None
		self.motto = ""
		self.phone_number = ""
		self.first_name = first_name
		self.last_name = last_name
		self.opt_in = opt_in
		self.fullname_privacy = False
		self.age_restricted = age_restricted
	
	def set_gamertag(self, gamertag):
		if not validate_gamertag(gamertag): raise ValidationError("Invalid gamer tag!")
		if database.exists(self.__class__, "gamertag", gamertag): raise UserExistsError("That username is already taken!")
		self.gamertag = gamertag
	
	def set_password(self, password):
		if not validate_password(password): raise ValidationError("Invalid password!")
		self.password = password.hash(password)
	
	def set_email(self, email):
		if not validate_email(email): raise ValidationError("Invalid email!")
		self.email = email
		self.email_hash = hashlib.sha1(bytes(email, 'utf-8')).hexdigest()
	
	def get_profile(self, private=False):
		result = {
			"user_id": self.id,
			"gamertag": self.gamertag,
			"badge_id": self.badge_id,
			"photo_url": None, # It's not really ready yet...
			"motto": self.motto,
			"email_hash": self.email_hash,
			"first_name": self.first_name,
			"lite": False, # TODO We don't support lite accounts yet :(
			"capabilities": {"push_notifications": 0},
			"gamerscore": self.score,
			"level_position": self.level,
			
			# Junk data
			"level_name": "Trogdor",
			"level_points": 350,
			"level_next_points": 1000,
		}
		
		if private:
			result['email'] = self.email
			result['phone_number'] = self.phone_number
			result['password'] = self.password
			result['last_name'] = self.last_name
			result['opt_in'] = False
			result['fullname_privacy'] = self.fullname_privacy
			result['age_restricted'] = self.age_restricted
		else:
			result['last_name'] = self.last_name if not self.fullname_privacy else ""
		
		return result
	
	def check_password(self, cand):
		try:
			return password.verify(self.password, cand)
		except password.IncorrectPasswordError:
			return False
	
	def create_session(self):
		session = Session(self)
		database.add(session)
		return session
	
	@classmethod
	def current(self):
		return Session.current().user
	
	@classmethod
	def login(self, gamertag, password):
		try:
			user = database.find_one(self, "gamertag", gamertag)
			if user.check_password(password):
				session = self.create_session()
				return user, session
			else:
				raise LoginError("Your username wasn't found or your password wasn't valid.")
		except:
			raise LoginError("Your username wasn't found or your password wasn't valid.")
	

bp = Blueprint(__name__, __name__)

@bp.post("/<int:version>/<appname>/users")
def users_register(version, appname):
	form_dict = request.form.to_dict()
	info = {}
	
	for k in form_dict:
		if k.startswith("user["):
			info[k[5:-1]] = form_dict[k]
	
	# result = User.register(user_info)
	
	if info["password"] != info["password_confirmation"]:
		plus_error(400, "Passwords do not match")
	
	try:
		user = User(info["gamertag"], info["password"], info["email"], info.get("first_name", ""), info.get("last_name", ""))
	except ValidationError as e:
		plus_error(400, e.msg)
	except UserExistsError as e:
		plus_error(400, "User already exists")
	except Exception as e:
		plus_error(500, "Internal server error")
	
	database.add(user)
	session = user.create_session()
	database.commit()
	
	return make_login_response(user, session)

@bp.get("/<int:version>/<appname>/user_updates")
def get_user_updates(version, appname):
	user = User.current()
	
	# Yet another mostly filler response...
	return {
		"success": True,
		"online_friends": [],
		"updates": [],
		"update_interval": PLUS_USER_UPDATE_INTERVAL,
	}

"""
class User_old(Persistent):
	def on_init(self):
		self.gamertag = ""
		self.badge_id = ""
		self.photo_url = ""
		self.motto = ""
		self.email = ""
		self.email_hash = ""
		self.phone_number = ""
		self.password = ""
		self.first_name = ""
		self.last_name = ""
		self.opt_in = False
		self.fullname_privacy = False
		self.age_restricted = False
	
	def on_load(self):
		# Some earlier versions had age restricted set to a different type
		self.age_restricted = bool(self.age_restricted)
		
		pass
	
	def get_id(self):
		return self._id
	
	def set_gamertag(self, tag):
		if not validate_gamertag(tag):
			raise ValidationError("Invalid gamertag")
		
		self.gamertag = tag
	
	def set_password(self, pw):
		if not validate_password(pw):
			raise ValidationError("Invalid password")
		
		self.password = password.hash(pw)
	
	def check_password(self, cand):
		try:
			return password.verify(self.password, cand)
		except password.IncorrectPasswordError:
			return False
	
	def set_email(self, email):
		if not validate_email(email):
			raise ValidationError("Invalid email")
		
		self.email = email
		self.email_hash = sha1(email)
	
	def set_motto(self, motto):
		self.motto = motto
	
	def set_phone_number(self, pn):
		self.phone_number = pn
	
	def set_badge_url(self, url):
		self.badge_id = url
	
	def set_real_name(self, first, last):
		self.first_name = first
		self.last_name = last
	
	def set_fullname_privacy(self, value):
		self.fullname_privacy = int(value)
	
	def set_age_restricted(self, ar):
		self.age_restricted = int(ar)
	
	def set_opt_in(self, optin):
		self.opt_in = not not optin
	
	def to_dict(self, private=False):
		current_user = User.current(False)
		
		result = {
			"user_id": self._id,
			"gamertag": self.gamertag,
			"badge_id": self.badge_id,
			"photo_url": self.photo_url,
			"motto": self.motto,
			"email_hash": sha1(self.email),
			"first_name": self.first_name,
			"lite": False,
			"capabilities": {"push_notifications": 0},
			"gamerscore": 0,
			"level_position": 0,
			"level_name": "Trogdor",
			"level_points": 0,
			"level_next_points": 1000,
		}
		
		if private:
			result['email'] = self.email
			result['phone_number'] = self.phone_number
			result['password'] = self.password
			result['last_name'] = self.last_name
			result['opt_in'] = False
			result['fullname_privacy'] = self.fullname_privacy
			result['age_restricted'] = self.age_restricted
		else:
			result['last_name'] = self.last_name if not self.fullname_privacy else ""
		
		return result
	
	@classmethod
	def register(self, user_info):
		"Try to register as the given user."
		
		gamertag = user_info["gamertag"]
		email = user_info["email"]
		password = user_info["password"]
		
		# Make sure password matches the confirmation, if there is one.
		if ("password_confirmation" in user_info):
			if (user_info["password"] != user_info["password_confirmation"]):
				raise PasswordsDoNotMatchError("Passwords do not match")
		
		# Make sure gamertag is unique
		if (self.lookup({"gamertag": gamertag}) != None):
			raise UserExistsError("A user with that gamertag already exists.")
		
		# Make sure email is unique
		if (self.lookup({"email": email})):
			raise EmailUsedError("Someone has already used that email to register.")
		
		user = self()
		user.set_gamertag(gamertag)
		user.set_email(email)
		user.set_password(password)
		user.set_motto(user_info.get("motto", ""))
		user.set_badge_url(user_info.get("badge_id", ""))
		user.set_real_name(user_info.get("first_name", ""), user_info.get("last_name", ""))
		user.set_age_restricted(user_info.get("age_restricted", 0))
		user.set_opt_in(user_info.get("opt_in", 1))
		user.save()
		
		session = UserSession.new(user)
		
		return UserAndSession(user, session)
	
	@classmethod
	def login(self, gamertag, password):
		"Try to log in as the given user. Returns the new session."
		
		user = self.lookup({"gamertag": gamertag})
		
		if not user:
			raise LoginError(f"No such user: {gamertag}")
		
		correct = user.check_password(password)
		
		if not correct:
			raise LoginError(f"Wrong password")
		
		session = UserSession.new(user)
		
		return UserAndSession(user, session)
	
	@classmethod
	def current(self, throw = True):
		" ""
		Get the current user
		
		throw: If an exception should be raised instead of returning None when
		there is no current user.
		" ""
		
		session = UserSession.current(throw)
		
		if not session:
			return None
		
		return session.get_user()
"""

"""
class UserSession(Persistent):
	def on_init(self):
		self.token = None
		self.user = None
		self.expire = int(time.time()) + PLUS_SESSION_TIME
	
	def validate(self):
		""
		Make sure this session is allowable.
		""
		
		if (self.token == None or self.user == None or (PLUS_SESSION_EXPIRY and self.expire < int(time.time()))):
			self.delete()
			return False
		
		return True
	
	def get_user(self):
		""
		Get the user associated with the session
		""
		
		try:
			return User(self.user)
		except:
			return None
	
	def get_token(self):
		""
		Get the login token
		""
		
		return self.token
	
	@classmethod
	def new(self, user):
		""
		Make a new session for the given user
		""
		
		session = self()
		session.token = secrets.token_hex(PLUS_SESSION_TOKEN_BITS >> 3).upper()
		session.user = user._id
		session.save()
		
		return session
	
	@classmethod
	def current_(self):
		""
		Get the current session, if still valid, otherwise return None
		""
		
		try:
			token = request.authorization.get("oauth_token", None)
		except AttributeError:
			return None
		
		if not token:
			return None
		
		session = self.lookup({"token": token})
		
		if not session:
			return None
		
		if not session.validate():
			return None
		
		return session
	
	@classmethod
	def current(self, throw=True):
		""
		Same as current_() but with the option to throw an exception instead
		of reutrning None.
		""
		
		session = self.current_()
		
		if not session and throw:
			raise SessionError("There is no current session")
		
		return session
"""

"""
def make_login_response(user, session):
	"Make a login response given the user and session"
	
	response = {
		"success": True,
		"auth_token": session.get_token(),
		"oauth_token": session.get_token(),
		"oauth_secret": "totally_real_oauth_secret",
		"user_id": user.get_id(),
	}
	
	response["configuration"] = {}
	response["messages"] = [
		{
			"title": "Katten Server",
			"text": "Welcome to Katten server!",
			"url": "https://example.com",
			"alert": True,
			"web_view": False,
		}
	]
	response["profile"] = user.to_dict(True)
	
	return response

class UserAppDataEntry(Persistent):
	"A key->value data pair stored in Plus+ for use by games."
	
	def on_init(self):
		self.game = None
		self.user = None
		self.key = None
		self.privacy = 0
		self.value = None
	
	@classmethod
	def set(self, game, user_id, key, privacy, value):
		# try to load current value
		entry = self.lookup({"game": game, "user": user_id, "key": key})
		
		if not entry:
			entry = self()
		
		entry.game = game
		entry.user = user_id
		entry.key = key
		entry.privacy = privacy
		entry.value = base64.b64encode(value)
		
		entry.save()
	
	@classmethod
	def get(self, game, user_id, key):
		entry = self.lookup({"game": game, "user": user_id, "key": key})
		
		if not entry:
			return None
		
		# TODO privacy stuff, probably
		
		return base64.b64decode(entry.value)

__all__ = list(globals().keys())
"""
