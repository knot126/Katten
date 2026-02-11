import database
from game import Game
from user import User
from database import Model, Column, String, Integer, ForeignKey, relationship

class Datum(Model):
	__tablename__ = "datums"
	
	id = Column(Integer, primary_key=True)
	game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	key = Column(String, nullable=False)
	value = Column(String, nullable=False)
	privacy = Column(Integer, nullable=False)
	
	game = relationship(Game)
	user = relationship(User, back_populates="datums")
	
	def __init__(self, user, game, key, value, privacy):
		self.user = user
		self.game = game
		self.key = key
		self.value = value
		self.privacy = privacy
