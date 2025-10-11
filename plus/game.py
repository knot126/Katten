"""
App and game info and registration
"""

from database import Model, Column, Integer, String, Boolean
import asset

class Game(Model):
	__tablename__ = "games"
	
	id = Column(Integer, primary_key=True)
	app_key = Column(String(30), unique=True, nullable=False)
	name = Column(String(30), nullable=False)
	icon = relationship(asset.Asset)
	publisher = Column(String(30), nullable=False)
	# catalog url, feed url
	app_store_url = Column(String(1000), nullable=False)
	# mpid
	featured = Column(Boolean, nullable=False)
	# leaderboard info
	
	def __init__(self, app_key, name, icon, featured=False, publisher="ngmoco", app_store_url="https://apps.apple.com/us/app/smash-hit/id603527166"):
		self.app_key = app_key
		self.name = name
		self.icon = icon
		self.publisher = publisher
		self.featured = featured
		self.app_store_url = app_store_url
	
	def to_dict(self):
		game = {}
		game["icon_url"] = f"http://{request.host}/static/badges/0.png" if not self.icon_url else self.icon_url
		game["catalog_url"] = ""
		game["feed_url"] = ""
		game["leaderboards_count"] = 0
		game["achievements_count"] = 0
		game["app_store_url"] = ""
		game["master_product_id"] = game["_id"]
		return game
