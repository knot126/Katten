import database
from database import Model, Column, String, Integer, ForeignKey, relationship
from flask import Blueprint, request
from user import User

class Buddy(Model):
	__tablename__ = "buddies"
	
	from_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
	to_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
	type = Column(String(12), nullable=False)
	
	from_user = relationship("User", back_populates="buddies", foreign_keys="Buddy.from_user_id")
	to_user = relationship("User", foreign_keys="Buddy.to_user_id")
	
	def __init__(self, from_user, to_user, type):
		self.from_user = from_user
		self.to_user = to_user
		self.type = type
	
	@classmethod
	def exists(self, from_user, to_user):
		return database.session.query(self).filter(self.from_user_id == first, self.to_user_id == second).first() != None

bp = Blueprint(__name__, __name__)

@bp.post("/<int:version>/<appname>/users/<int:user_id>/buddies")
def post_users_buddies(version, appname, user_id):
	me = User.current()
	buddy = User.get(int(request.form['id']))
	type = 'enemies' if request.form['enemy'] == 'true' else 'friends'
	
	# TODO handle existing relationships (tho it's probably fine as is)
	database.add(Buddy(me, buddy, type))
	database.add(Buddy(buddy, me, type))
	database.commit()
	
	return {
		"success": True,
		"buddy": buddy.get_profile(),
	}

@bp.get("/<int:version>/<appname>/users/<int:user_id>/buddies")
def get_users_buddies(version, appname, user_id):
	user = User.current()
	relation = int(request.form['relation'])
	offset = int(request.form['offset'])
	count = int(request.form['count'])
	
	buds = user.buddies[offset:offset+count]
	
	return {
		"success": True,
		"list": [bud.to_user.get_profile() for bud in buds if bud.type == relation]
	}
