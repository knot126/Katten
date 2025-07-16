"""
App and game info and registration
"""

from persist import Persistent

class Game(Persistent):
	def on_init(self):
		self.app_key = None
		self.name = ""
		self.icon_url = ""
		# self.catalog_url = ""
		# self.feed_url = ""
		self.featured = False
		self.publisher = ""
		# self.app_store_url = ""
		# self.master_product_id = ""
	
	def to_dict(self):
		game = self.__dict__.copy()
		game["icon_url"] = f"http://{request.host}/static/badges/0.png" if not self.icon_url else self.icon_url
		game["catalog_url"] = ""
		game["feed_url"] = ""
		game["leaderboards_count"] = 0
		game["achievements_count"] = 0
		game["app_store_url"] = ""
		game["master_product_id"] = game["_id"]
		return game
	
	@classmethod
	def new(self, app_key, name=None):
		game = self()
		game.app_key = app_key
		game.name = name or app_key
		game.save()
		return game
