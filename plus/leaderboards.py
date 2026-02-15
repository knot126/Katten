from config import *
from flask import Blueprint, request
from database import Model, Table, Column, Integer, String, Boolean, ForeignKey, NoResultFound, relationship, desc
from asset import Asset
from game import Game
from user import User
import database

bp = Blueprint(__name__, __name__)

class Leaderboard(Model):
	__tablename__ = "leaderboards"
	
	game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)
	level = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	icon_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
	
	game = relationship("Game", back_populates="leaderboards")
	icon = relationship(Asset)
	
	def __init__(self, game, level, title, icon=None):
		self.game = game
		self.level = level
		self.title = title
		self.icon = icon
	
	def get_object(self, user_id=None):
		score = Score.find_all(self.game, self.level, 0, 1)
		score = score[0] if len(score) > 0 else None
		
		try:
			if user_id:
				score = Score.find(self.game, self.level, User.get(user_id))
		except:
			pass
		
		return {
			"score": score.to_object() if score else None,
			"level": self.level,
			"title": self.title,
			"icon_url": self.icon.get_url() if self.icon else None,
		}
	
	@classmethod
	def find(self, game, level):
		try:
			return database.session.query(self).filter(self.game_id == game.id, self.level == level).one()
		except NoResultFound as e:
			if PLUS_AUTO_REGISTER_LEADERBOARDS:
				leaderboard = self(game, level, f"Leaderboard {level}")
				database.add(leaderboard)
				database.commit()
				return leaderboard
			else:
				raise e
	
	@classmethod
	def find_all(self, game):
		return database.session.query(self).filter(self.game_id == game.id).all()

class Score(Model):
	__tablename__ = "scores"
	
	game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)
	level = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
	score = Column(Integer, nullable=False)
	
	game = relationship("Game")
	user = relationship("User")
	
	def __init__(self, game, level, user, score):
		self.game = game
		self.level = level
		self.user = user
		self.score = score
	
	def to_object(self):
		return {
			"score": self.score,
			"formatted_score": str(self.score),
			"user_id": self.user.id,
			"gamertag": self.user.gamertag,
			"badge_id": self.user.get_badge_url(),
			"rank": 1, #TODO
		}
	
	@classmethod
	def find(self, game, level, user):
		return database.session.query(self).filter(self.game_id == game.id, self.level == level, self.user_id == user.id).one()
	
	@classmethod
	def find_all(self, game, level, offset, limit):
		return database.session.query(self).filter(self.game_id == game.id, self.level == level).order_by(desc(self.score)).offset(offset).limit(limit).all()
	
	@classmethod
	def create_or_update(self, game, level, user, score):
		try:
			sc = self.find(game, level, user)
			sc.score = score
			return sc
		except NoResultFound as e:
			sc = self(game, level, user, score)
			database.add(sc)
			return sc

@bp.post("/<int:version>/<appname>/games/<app_key>/leaderboards/<int:leaderboard_index>/scores")
def submit_score(version, appname, app_key, leaderboard_index):
	user = User.current()
	game = Game.find(app_key)
	Leaderboard.find(game, leaderboard_index) # assert that the leaderboard exists :3
	sc = Score.create_or_update(game, int(request.form["level"]), user, int(request.form["score"]))
	database.commit()
	return {"success": True, "score": sc.to_object()}

@bp.get("/<int:version>/<appname>/games/<app_key>/leaderboards/<int:leaderboard_index>")
def get_leaderboard_scores(version, appname, app_key, leaderboard_index):
	# TODO: Implement support for request.args['relation']=='friends'!!!
	user = User.current()
	count = int(request.args['count'])
	offset = int(request.args['offset'])
	game = Game.find(app_key)
	
	leaderboard = Leaderboard.find(game, leaderboard_index)
	scores = Score.find_all(game, leaderboard_index, offset, count)
	user_score = Score.find(game, leaderboard_index, user)
	
	return {
		"success": True,
		"leaderboard": [s.to_object() for s in scores],
		"title": leaderboard.title,
		"level": leaderboard.level,
		"icon_url": leaderboard.icon.get_url() if leaderboard.icon else None,
		"user_score": user_score.to_object(),
		"offset": offset,
		"total": len(scores),
	}

@bp.get("/<int:version>/<appname>/games/<app_key>/leaderboards")
def get_leaderboards(version, appname, app_key):
	# TODO: Requests /1/Rolando/games/(null)/leaderboards?user_id=<id> and fucking dies
	game = Game.find(app_key)
	user_id = request.args.get("user_id", None)
	user_id = int(user_id) if user_id != None else user_id
	
	return {
		"success": True,
		"leaderboards": [lb.get_object(user_id) for lb in Leaderboard.find_all(game)],
	}
