import database
from database import Model, Column, Boolean, String, Integer

class SystemMessage(Model):
	__tablename__ = "system_messages"
	
	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	text = Column(String, nullable=False)
	url = Column(String, nullable=False)
	alert = Column(Boolean, nullable=False)
	web_view = Column(Boolean, nullable=False)
	enabled = Column(Boolean, nullable=False)
	
	def __init__(self, title, text, url, alert, web_view):
		self.title = title
		self.text = text
		self.url = url
		self.alert = alert
		self.web_view = web_view
		self.enabled = True
	
	def get_dict(self):
		return {
			"title": self.title,
			"text": self.text,
			"url": self.url,
			"alert": self.alert,
			"web_view": self.web_view,
		}
	
	@classmethod
	def create(self, title, text, url, alert, web_view):
		database.add(self(title, text, url, alert, web_view))
	
	@classmethod
	def current_messages(self):
		return [msg.get_dict() for msg in database.session.query(self).all() if msg.enabled]
