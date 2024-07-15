import time

class User(Persistent):
	def on_init(self):
		self.gamertag = ""
		self.badge_id = 0
		self.photo_url = ""
		self.motto = ""
		self.email = ""
		self.phone_number = ""
		self.password = ""
		self.first_name = "New"
		self.last_name = "Gamer"
		self.fullname_privacy = False
		self.age_restricted = False

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
