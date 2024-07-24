"""
App and game info and registration
"""

class Game(Persistent):
	def on_init(self):
		self.app_key = None
		self.name = ""
		# self.icon_url = ""
		# self.catalog_url = ""
		# self.feed_url = ""
		self.featured = False
		# self.leaderboards_count = 0
		# self.achievements_count = 0
		self.publisher = ""
		# self.app_store_url = ""
		# self.master_product_id = ""
	
	def to_dict(self):
		game = self.__dict__.copy()
		game["icon_url"] = f"http://{request.host}" + url_for("static", filename = "0.png")
		game["catalog_url"] = ""
		game["feed_url"] = ""
		game["leaderboards_count"] = 0
		game["achievements_count"] = 0
		game["app_store_url"] = ""
		game["master_product_id"] = game["app_key"]
		return game
	
	@classmethod
	def new(self, app_key, name=None, icon_url=None, featured=False, publisher=None, ):
		game = self()
		game.app_key = app_key
		game.name = name or app_key
		game.featured = featured
		game.publisher = publisher
		game.save()
		return game
