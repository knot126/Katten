from config import *
import time
import argon2
import secrets
import re
from collections import namedtuple

def password_hash(password):
	ph = argon2.PasswordHasher()
	return ph.hash(password)

def password_verify(hash, candidate):
	ph = argon2.PasswordHasher()
	return ph.verify(hash, candidate)

def validate_gamertag(gamertag):
	return re.match(r"[a-zA-Z0-9]{" + str(PLUS_GAMERTAG_MIN_LENGTH) + "," + str(PLUS_GAMERTAG_MAX_LENGTH) + r"}", gamertag) != None

def validate_password(password):
	return len(password) >= PLUS_PASSWORD_MIN_LENGTH

def validate_email(email):
	# Note: This only validates a subset of emails, to keep things simple.
	return re.match(r"^[a-zA-Z0-9\_\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\.\-]+$", email) != None

def validate_first_or_last(first_or_last):
	return re.match(r"^[A-Z][a-z]*$", first_or_last) != None

class ValidationError(Exception): pass
class UserExistsError(Exception): pass
class InvalidUserError(Exception): pass
class PasswordsDoNotMatchError(Exception): pass
class EmailUsedError(Exception): pass
class LoginError(Exception): pass

UserAndSession = namedtuple("UserAndSession", "user session")

class User(Persistent):
	def on_init(self):
		self.gamertag = ""
		self.badge_id = ""
		self.photo_url = ""
		self.motto = ""
		self.email = ""
		self.phone_number = ""
		self.password = ""
		self.first_name = ""
		self.last_name = ""
		self.opt_in = False
		self.fullname_privacy = 0
		self.age_restricted = 0
	
	def on_load(self):
		print(self.__dict__)
	
	def get_id(self):
		return self._id
	
	def set_gamertag(self, tag):
		if not validate_gamertag(tag):
			raise ValidationError("Invalid gamertag")
		
		self.gamertag = tag
	
	def set_password(self, pw):
		if not validate_password(pw):
			raise ValidationError("Invalid password")
		
		self.password = password_hash(pw)
	
	def check_password(self, cand):
		try:
			return password_verify(self.password, cand)
		except argon2.exceptions.VerifyMismatchError:
			return False
	
	def set_email(self, email):
		if not validate_email(email):
			raise ValidationError("Invalid email")
		
		self.email = email
	
	def set_motto(self, motto):
		self.motto = motto
	
	def set_badge_url(self, url):
		self.badge_id = url
	
	def set_real_name(self, first, last):
		self.first_name = first
		self.last_name = last
	
	def set_age_restricted(self, ar):
		self.age_restricted = ar
	
	def set_opt_in(self, optin):
		self.opt_in = not not optin
	
	def to_dict(self):
		result = self.__dict__.copy()
		del result["_id"]
		del result["_ver"]
		del result["password"]
		return result
	
	@classmethod
	def register(self, user_info):
		"""
		Try to register as the given user.
		"""
		
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
		"""
		Try to log in as the given user. Returns the new session.
		"""
		
		user = self.lookup({"gamertag": gamertag})
		
		if not user:
			raise LoginError(f"No such user: {gamertag}")
		
		correct = user.check_password(password)
		
		if not correct:
			raise LoginError(f"Wrong password")
		
		session = UserSession.new(user)
		
		return UserAndSession(user, session)
	
	@classmethod
	def current(self):
		"""
		Get the current user
		"""
		
		session = UserSession.current()
		
		if not session:
			return None
		
		return session.get_user()

class UserSession(Persistent):
	def on_init(self):
		self.token = None
		self.user = None
		self.expire = int(time.time()) + PLUS_SESSION_TIME
	
	def validate(self):
		"""
		Make sure this session is allowable.
		"""
		
		if (self.token == None or self.user == None or self.expire < int(time.time())):
			self.delete()
			return False
		
		return True
	
	def get_user(self):
		"""
		Get the user associated with the session
		"""
		
		try:
			return User(self.user)
		except:
			return None
	
	def get_token(self):
		"""
		Get the login token
		"""
		
		return self.token
	
	@classmethod
	def new(self, user):
		"""
		Make a new session for the given user
		"""
		
		session = self()
		session.token = secrets.token_hex(PLUS_SESSION_TOKEN_BITS >> 3).upper()
		session.user = user._id
		session.save()
		
		return session
	
	@classmethod
	def current(self):
		"""
		Get the current session, if still valid, otherwise return None
		"""
		
		token = request.authorization.get("oauth_token", None)
		
		if not token:
			return None
		
		session = self.lookup({"token": token})
		
		if not session:
			return None
		
		if not session.validate():
			return None
		
		return session

def make_login_response(user, session):
	"""
	Make a login response given the user and session
	"""
	
	response = {
		"success": True,
		"auth_token": "totally_real_auth_token",
		"oauth_token": session.get_token(),
		"oauth_secret": "totally_real_oauth_secret",
		"user_id": user.get_id(),
	}
	
	response["messages"] = [
		{
			"title": "Katten Server",
			"text": "Welcome to Katten server!",
			"url": "https://example.com",
			"alert": True,
			"web_view": False,
		}
	]
	response["profile"] = user.to_dict()
	
	return response
