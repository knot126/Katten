import math
import database
from database import Model, Column, String, Integer, ForeignKey, relationship
from user import User
from time import time
from utils import *
from flask import Blueprint, request

bp = Blueprint(__name__, __name__)

class Flag(Model):
	__tablename__ = "flags"
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	reported_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	report_time = Column(Integer, nullable=False)
	reason = Column(String(2000), nullable=False)
	
	user = relationship(User, back_populates="submitted_reports")
	reported_user = relationship(User, back_populates="reports")
	
	def __init__(self, user, reported_user, reason):
		self.user = user
		self.reported_user = reported_user
		self.report_time = math.floor(time())
		self.reason = reason
	
	@classmethod
	def create(self, reported_user, reason):
		flag = Flag(User.current(), reported_user, reason)
		database.add(flag)

@bp.put("/<int:version>/<appname>/users/<int:user_id>/flags")
def put_user_flag(version, appname, user_id):
	Flag.create(User.get(user_id), request.body["reason"])
	database.commit()
