"""
Account and user related stuff
"""

from config import *
from utils import *
# from persist import Persistent
import database
from database import NoResultFound, Model, Column, String, Integer, Boolean, ForeignKey, relationship, text
from asset import Asset, upload
from utils import *
from flask import Blueprint, request
import traceback
import time
import password
import secrets
import re
import base64
import hashlib

import game
import asset
import badge

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
	gamertag = Column(String(PLUS_GAMERTAG_MAX_LENGTH), nullable=False, unique=True, index=True)
	score = Column(Integer, nullable=False)
	level = Column(Integer, nullable=False)
	badge_id = Column(Integer, nullable=False)
	photo_id = Column(Integer, ForeignKey("assets.id"))
	motto = Column(String)
	email = Column(String, nullable=False, unique=True)
	email_hash = Column(String, nullable=False, index=True)
	phone_number = Column(String)
	password = Column(String, nullable=False)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=False)
	opt_in = Column(Boolean, nullable=False)
	fullname_privacy = Column(Boolean, nullable=False)
	age_restricted = Column(Boolean, nullable=False)
	
	games = relationship("Game", secondary=game.user_games, back_populates="players")
	sessions = relationship("Session", back_populates="user")
	datums = relationship("Datum", back_populates="user", lazy=True)
	buddies = relationship("Buddy", back_populates="from_user", foreign_keys="Buddy.from_user_id", lazy=True)
	
	flags = relationship("Flag", back_populates="reported_user", foreign_keys="Flag.reported_user_id", lazy=True)
	submitted_flags = relationship("Flag", back_populates="user", foreign_keys="Flag.user_id", lazy=True)
	
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
	
	def set_password(self, passwd):
		if not validate_password(passwd): raise ValidationError("Invalid password!")
		self.password = password.hash(passwd)
	
	def set_email(self, email):
		if self.email == email: return
		if not validate_email(email): raise ValidationError("Invalid email!")
		if database.exists(self.__class__, "email", email): raise EmailUsedError("Email is already registered!")
		self.email = email
		self.email_hash = hashlib.sha1(bytes(email, 'utf-8')).hexdigest().upper()
	
	def get_games(self):
		return [g.to_dict() for g in self.games]
	
	def get_badge_url(self):
		return f"http://{request.host}/static/badges/{self.badge_id}.png"
	
	def get_profile(self, private=False):
		result = {
			"user_id": self.id,
			"gamertag": self.gamertag,
			"badge_id": self.get_badge_url(),
			"photo_url": None, # It's not really ready yet...
			"motto": self.motto,
			"email_hash": self.email_hash,
			"first_name": self.first_name,
			"games": self.get_games(),
			"lite": False, # TODO We don't support lite accounts yet :(
			"capabilities": {"push_notifications": 0},
			"gamerscore": self.score,
			"level_position": self.level,
			
			# Junk data
			"level_name": "Trogdor",
			"level_points": 1000,
			"level_next_points": 350,
		}
		
		if private:
			result['email'] = self.email
			result['phone_number'] = self.phone_number
			# result['password'] = self.password
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
	
	def is_friends_with(self, other):
		return False
	
	@classmethod
	def current(self):
		return Session.current().user
	
	@classmethod
	def find(self, gamertag):
		return database.find_one(self, "gamertag", gamertag)
	
	@classmethod
	def login(self, gamertag, password):
		try:
			user = database.find_one(self, "gamertag", gamertag)
			if user.check_password(password):
				session = user.create_session()
				return user, session
			else:
				print("Wrong password")
				raise LoginError("Your username wasn't found or your password wasn't valid.")
		except:
			print("Gamertag not found")
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
		traceback.print_exc()
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

# @bp.get("/<int:version>/<appname>/users/<int:user_id>/buddies")
# def users_buddies(version, appname, user_id):
# 	user = User.current()
# 	
# 	return {
# 		"success": True,
# 		"list": [],
# 		"offset": 0,
# 		"total": 0,
# 	}

@bp.post("/<int:version>/<appname>/session")
def session_init(version, appname):
	def attempt_to_add_game(session):
		# Attempt to add game to user's account if they don't already have it
		try:
			app = Game.find(appname)
			
			# its not broken anymore :D
			if app not in session.user.games:
				session.user.games.append(app)
				# print("USER GAMES!!!", session.user.games)
				database.commit()
		except:
			pass
	
	# Katten doesn't really care about OAuth 1.0's signing things; it's only
	# relevant over an insecure HTTP connection anyway.
	
	# If there is an auth_token instead of gamertag and password then we're
	# logging in using an existing session.
	if "auth_token" in request.form:
		try:
			session = Session.find(request.form["auth_token"])
			attempt_to_add_game(session)
		except:
			plus_error(401, "Session is not valid")
		
		return make_login_response(session.user, session)
	else:
		try:
			user, session = User.login(request.form["gamertag"], request.form["password"])
			attempt_to_add_game(session)
			database.commit()
			return make_login_response(user, session)
		except:
			traceback.print_exc()
			plus_error(1, "Wrong username or password")

@bp.post("/<int:version>/<appname>/oauth/authorize_new")
def oauth_authorize_new(version, appname):
	"""
	This should do something oauth related but we can just return the typcial
	login response.
	"""
	
	try:
		session = Session.current()
	except:
		plus_error(401, "Session is not valid")
	
	app = Game.find(appname)
	
	if app not in session.user.games:
		session.user.games.append(app)
		database.commit()
	
	return make_login_response(session.user, session)

@bp.post("/<int:version>/<appname>/users/validate")
def users_validate(version, appname):
	"""
	Validate if a user's name, email, etc are valid
	"""
	
	field = request.form["field"]
	value = request.form["value"]
	
	msg = "Unknown field"
	
	match field:
		case "gamertag":
			msg = None if validate_gamertag(value) else "Invalid gamertag"
			if not msg:
				try:
					User.find(value)
					msg = "Gamertag already taken"
				except:
					msg = None
		case "password":
			msg = None if validate_password(value) else "Invalid password"
		case "email":
			msg = None if validate_email(value) else "Not a valid email"
		case "first_name" | "last_name":
			msg = None if validate_first_or_last(value) else f"Invalid {field.replace('_', ' ')}"
	
	return {"success": True} if not msg else {"success": False, "error": 1, "error_msg": msg}

@bp.get("/<int:version>/<appname>/users/search")
def users_search(version, appname):
	if "email_hash" in request.args:
		try:
			return {
				"success": True,
				"offset": 0,
				"list": [database.find_one(User, "email_hash", request.args['email_hash']).get_profile()]
			}
		except:
			pass
	
	if "gamertag" in request.args:
		expr = request.args['gamertag'].replace('*', '%')
		offset = int(request.args['offset'])
		limit = int(request.args['count'])
		
		objects = database.session.query(User).filter(text("gamertag LIKE :e")).params({"e": expr}).offset(offset).limit(limit).all()
		
		return {
			"success": True,
			"offset": offset,
			"list": [user.get_profile() for user in objects],
		}
	
	return {"success": True, "list": []}

@bp.get("/<int:version>/<appname>/users/<gamertag>")
def users_lookup_by_gamertag(version, appname, gamertag):
	try:
		user = User.find(gamertag)
	except:
		traceback.print_exc()
		plus_error(404, "Playername not found!")
	
	result = user.get_profile()
	result["success"] = True
	return result

@bp.get("/<int:version>/<appname>/users/<int:user_id>")
def users_lookup_by_id(version, appname, user_id):
	try:
		user = User.get(user_id)
	except:
		traceback.print_exc()
		plus_error(404, "Playername not found!")
	
	result = user.get_profile()
	result["success"] = True
	return result

@bp.get("/<int:version>/<appname>/users/<int:user_id>/games")
def get_user_games(version, appname, user_id):
	return {
		"success": True,
		"games": User.get(user_id).get_games(),
	}

def tobadgeid(v, fallback=0):
	# HACK again :(
	try:
		return int(v)
	except ValueError as e:
		for entry in badge.list_badges()["list"][0]["badges"]:
			if v == entry["icon_url"]:
				return entry["id"]
		
		return fallback

@bp.put("/<int:version>/<appname>/users/<int:user_id>")
def users_update(version, appname, user_id):
	user = User.current()
	
	user_info = request.form.to_dict()
	
	user.motto = user_info.get("motto", user.motto)
	user.phone_number = user_info.get("phone_number", user.phone_number)
	user.badge_id = tobadgeid(user_info.get("badge_id", user.badge_id))
	user.first_name = user_info.get("first_name", user.first_name)
	user.last_name = user_info.get("last_name", user.last_name)
	user.fullname_privacy = int(user_info.get("fullname_privacy", user.fullname_privacy))
	
	user.set_email(user_info.get("email", user_info.get("email", user.email)))
	
	if ("password" in user_info and "password_confirmation" in user_info):
		if (user_info['password'] == user_info['password_confirmation']):
			try:
				user.set_password(user_info["password"])
			except ValidationError:
				plus_error(1, "Password is too short")
		else:
			plus_error(1, "Passwords do not match")
	
	database.commit()
	
	return {"success": True}
