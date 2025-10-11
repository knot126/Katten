"""
Support for various types of publicly-accessable assets
"""

from config import *
import database
from database import Model, Column, Integer, String, session, select
from hashlib import sha256

class Asset(Model):
	__tablename__ = "assets"
	
	id = Column(Integer, primary_key=True)
	hash = Column(String(64), nullable=False)
	refs = Column(Integer, nullable=False)
	
	def __init__(self, hash, content):
		self.hash = hash
		self.refs = 1
	
	def inc():
		self.refs += 1
	
	def dec():
		self.refs -= 1

def upload(data):
	hash = sha256(content).hexdigest()
	
	database.exists(Asset, "hash", )
	
	asset = Asset(data)
	session.add()
