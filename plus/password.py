"""
Simple password hashing and verification wrapper
"""

try:
	import argon2
except ModuleNotFoundError:
	print("Warning: Argon2 hashing is not available! A built in password hashing function will be used, but it is much less secure and is only meant for development, and any existing argon2 password hashes in the database won't work.")

import secrets
import hashlib
from base64 import b64encode, b64decode

class IncorrectPasswordError(Exception): pass

def hash(password):
	if 'argon2' in globals():
		ph = argon2.PasswordHasher()
		return ph.hash(password)
	else:
		salt = secrets.token_bytes(16)
		h = hashlib.sha256(salt + bytes(password, 'utf-8')).digest()
		return ':'.join(['basic', str(b64encode(h), 'utf-8'), str(b64encode(salt), 'utf-8')])

def verify(hash, candidate):
	if not hash.startswith("basic:"):
		if 'argon2' in globals():
			try:
				ph = argon2.PasswordHasher()
				return ph.verify(hash, candidate)
			except argon2.exceptions.VerifyMismatchError:
				raise IncorrectPasswordError('Passwords do not match')
		else:
			raise IncorrectPasswordError('Argon2 is not available')
	else:
		p = hash.split(':')
		h, salt = b64decode(p[1]), b64decode(p[2])
		candh = hashlib.sha256(salt + bytes(candidate, 'utf-8')).digest()
		if h == candh:
			return True
		else:
			raise IncorrectPasswordError('Passwords do not match')
