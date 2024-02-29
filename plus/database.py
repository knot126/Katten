import sqlite3

class Database():
	def __init__(self, name = "plusplus"):
		self.db = sqlite3.connect(f"../{name}.db")
		self.cur = self.db.cursor()
	
	def __del__(self):
		self.db.close()
	
	def run(self, qs, args = []):
		"""
		Execute sql statement and return results
		"""
		
		return self.cur.execute(qs, args).fetchall()
	
	def do(self, qs, *args):
		return self.run(qs, args)
