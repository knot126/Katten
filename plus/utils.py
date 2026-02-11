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

def make_login_response(user, session):
	"Make a login response given the user and session"
	
	from system_message import SystemMessage
	
	response = {
		"success": True,
		"user_id": user.id,
		"auth_token": session.token,
		"oauth_token": session.token,
		"oauth_secret": "totally_real_oauth_secret",
		"configuration": {},
		"messages": SystemMessage.current_messages(),
	}
	
	response["profile"] = user.get_profile(True)
	
	return response

def sha1(d):
	if type(d) == str: d = bytes(d, 'utf-8')
	return hashlib.sha1(d).hexdigest().upper()

def unixtime():
	return int(time.time())

__all__ = ["plus_error", "sha1", "unixtime", "make_login_response"]
