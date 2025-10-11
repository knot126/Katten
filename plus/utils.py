"""
Basic utilities for the Plus+ server
"""

from flask import make_response
from werkzeug.exceptions import HTTPException
import hashlib
import time

def plus_error(code, msg, extra={}):
	raise HTTPException(msg, make_response({
		"success": False,
		"error": code,
		"error_msg": msg,
	} | extra))

def sha1(d):
	if type(d) == str: d = bytes(d, 'utf-8')
	return hashlib.sha1(d).hexdigest().upper()

def unixtime():
	return int(time.time())

__all__ = list(globals().keys())
