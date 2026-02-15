"""
Support for various types of publicly-accessable assets
"""

from config import *
import database
import os
from database import Model, Column, Integer, String, session, select
from hashlib import sha256
from pathlib import Path
from flask import Blueprint, request

upload_dir = str(Path(PLUS_UPLOAD_DIRECTORY).expanduser())
os.makedirs(upload_dir, exist_ok=True)

class Asset(Model):
	__tablename__ = "assets"
	
	id = Column(Integer, primary_key=True)
	hash = Column(String(64), nullable=False)
	refs = Column(Integer, nullable=False)
	
	def __init__(self, hash, content):
		self.hash = hash
		self.refs = 1
		Path(f"{upload_dir}/{self.hash}").write_bytes(content)
	
	def inc(self):
		self.refs += 1
	
	def dec(self):
		self.refs -= 1
	
	def get_url(self):
		return f"http://{request.host}/user_uploads/{self.hash}"

def upload(data):
	hash = sha256(content).hexdigest()
	
	if database.exists(Asset, "hash", hash):
		asset = database.find(Asset, "hash", hash)[0]
		asset.inc()
	else:
		asset = Asset(data)
		session.add(asset)
	
	return asset

bp = Blueprint(__name__, __name__, static_url_path="/user_uploads", static_folder=upload_dir)
