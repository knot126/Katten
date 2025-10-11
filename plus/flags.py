from persist import Persistent
from utils import *
from flask import request

bp = Blueprint(__name__, __name__)

class Flag(Persistent):
	def on_init(self):
		self.user_id = 0
		self.reported_user = 0
		self.report_time = unixtime()
		self.reason = ""

@bp.put("/<int:version>/<appname>/users/<int:user_id>/flags")
def put_user_flag(version, appname, user_id):
	flag = Flag()
	flag.user_id = User.current().get_id()
	flag.reported_user = user_id
	flag.reason = request.body["reason"]
	flag.save()
