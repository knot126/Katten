import json

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
	
	def insert(self, db):
		db.run("""INSERT INTO users (gamertag, badge_id, photo_url, motto, email, phone_number, password, first_name, last_name, fullname_privacy, age_restricted) 
		               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [
			self.gamertag, self.badge_id, self.photo_url, self.motto, self.email, self.phone_number,
			self.password, self.first_name, self.last_name, self.fullname_privacy, self.age_restricted
		])
		
		r = db.run("""SELECT id FROM users WHERE gamertag = ?""", [self.gamertag])

class Session:
	def __init__(self):
		self.session_id = ""
		self.user_id = None
		self.extra = {}

class UserDB:
	def __init__(self, db):
		self.db = db
		
		self.spawn()
	
	def spawn(self):
		self.db.run("""
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER NOT NULL,
				gamertag VARCHAR(255) NOT NULL UNIQUE,
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
				user_id INTEGER,
				extra TEXT NOT NULL,
				PRIMARY KEY (id)
			);
		""")
	
	
	
	def insert_session(self, session):
		self.db.run("""INSERT INTO sessions VALUES (?, ?, ?)""", [session.session_id, session.user_id, json.dumps(session.extra)])
	
	def select(self, user):
		u = self.db.do("""SELECT * FROM users WHERE id = ?""", user.user_id)
	
	def select_session(self, user):
		
