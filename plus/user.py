class User:
	def __init__(self):
		self.user_id = 0
		self.gamertag = ""
		self.badge_id = ""
		self.photo_url = ""
		self.motto = ""
		self.email = ""
		self.phone_number = ""
		self.password = ""
		self.first_name = ""
		self.last_name = ""
		self.fullname_privacy = False
		self.age_restricted = False

class UserDB:
	def __init__(self, db):
		self.db = db
		
		self.spawn()
	
	def spawn(self):
		self.db.run("""
			CREATE TABLE IF NOT EXISTS users (
				id INT NOT NULL,
				gamertag VARCHAR(255) NOT NULL,
				badge_id TEXT(3000) NOT NULL,
				photo_url TEXT(3000) NOT NULL,
				motto VARCHAR(255) NOT NULL,
				email VARCHAR(255) NOT NULL,
				phone_number VARCHAR(20) NOT NULL,
				password VARCHAR(255) NOT NULL,
				first_name VARCHAR(100) NOT NULL,
				last_name VARCHAR(100) NOT NULL,
				fullname_privacy BOOLEAN NOT NULL,
				age_restricted BOOLEAN NOT NULL,
				PRIMARY KEY (id AUTOINCREMENT)
			);
			
			CREATE TABLE IF NOT EXISTS sessions (
				id TEXT NOT NULL,
				user_id INT,
				extra TEXT NOT NULL,
				PRIMARY KEY (id)
			);
		""")
	
	def insert(self, user):
		self.db.run("""INSERT INTO users (gamertag, badge_id, photo_url, motto, email, phone_number, password, first_name, last_name, fullname_privacy, age_restricted) 
		               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [
			user.gamertag, user.badge_id, user.photo_url, user.motto, user.email, user.phone_number,
			user.password, user.first_name, user.last_name, user.fullname_privacy, user.age_restricted
		])
	
	def select(self, user):
		
