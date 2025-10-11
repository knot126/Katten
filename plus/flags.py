from database import Model, Column, String, Integer
from utils import *
from flask import Blueprint, request

bp = Blueprint("flags", "flags")

class Flag(Model):
	__tablename__ = "flags"
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	reported_user = Column(Integer)
	report_time = Column(Integer, nullable=False)
	reason = Column(String(2000), nullable=False)

@bp.put("/<int:version>/<appname>/users/<int:user_id>/flags")
def put_user_flag(version, appname, user_id):
	flag = Flag()
	flag.user_id = User.current().get_id()
	flag.reported_user = user_id
	flag.reason = request.body["reason"]
	flag.save()
