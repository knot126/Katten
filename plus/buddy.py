import database
from database import Model, Column, String, Integer, ForeignKey, relationship
from flask import Blueprint, request

BUDDY_FRIEND = 0
BUDDY_ENEMY = 1
BUDDY_BLOCKED = 2

class Buddy(Model):
	__tablename__ = "buddies"
	
	from_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
	to_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
	relationship_type = Column(Integer, nullable=False)
	
	from_user = relationship("User", back_populates="buddies", foreign_keys="Buddy.from_user_id")
	to_user = relationship("User", back_populates="admirers", foreign_keys="Buddy.to_user_id")
	
	def __init__(self, first, second, type):
		if first > second: first, second = second, first
		self.first_user = first
		self.second_user = second
		self.relationship_type = type
