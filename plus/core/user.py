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

class Session(Persistent):
	def on_init(self):
		
