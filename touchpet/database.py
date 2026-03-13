from sys import argv, exit
from config import *
from pathlib import Path
from sqlalchemy import create_engine, Table, Boolean, Integer, String, Unicode, ForeignKey, select, text, desc
from sqlalchemy.schema import Column
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.exc import NoResultFound
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring as xml_tostring
import os
import re

__all__ = [
	"Table", "Boolean", "Integer", "String", "Unicode", "ForeignKey", "select",
	"text", "desc", "Column", "relationship", "NoResultFound", "Model",
	"Element", "xml_tostring",
]

os.makedirs(Path(TP_DATA_PATH).expanduser(), exist_ok=True)

TP_DATABASE_URI = TP_DATABASE_URI if TP_DATABASE_URI else (f"sqlite:///{Path(TP_DATA_PATH).expanduser()}/{TP_APPNAME}.db")

engine = create_engine(TP_DATABASE_URI)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class ModelBase:
	supports_properties = False
	
	def to_xml(self):
		root = Element(self.__class__.__name__.lower())
		
		for col in dir(self.__class__):
			# print(f"type of {col} is {type(getattr(self.__class__, col))}")
			if type(getattr(self.__class__, col)) == InstrumentedAttribute:
				e = Element(col)
				e.text = str(getattr(self, col))
				root.append(e)
		
		return root
	
	def to_inline_xml(self):
		element = Element(self.__class__.__name__.lower())
		
		for col in dir(self.__class__):
			if type(getattr(self.__class__, col)) == Column:
				element.set(col, str(getattr(self, col)))
		
		return element
	
	def assert_owned_by(self, playerID):
		assert(self.playerID == playerID)
	
	@classmethod
	def get1(self, id):
		return session.query(self).get(id)
	
	@classmethod
	def get2(self, feild_name, id):
		return session.query(self).where(getattr(self, idFieldName) == id).one()
	
	@classmethod
	def get(self, *args):
		if len(args) == 1:
			return self.get1(*args)
		else:
			return self.get2(*args)
	
	@classmethod
	def for_player(self, id):
		return session.query(self).where(self.playerID == id).all()
	
	@classmethod
	def for_pet(self, id):
		return session.query(self).where(self.petID == id).all()
	
	@classmethod
	def many_to_xml(self, objects):
		elements = Element(self.__tablename__)
		
		for obj in objects:
			elements.append(obj.to_xml())
		
		return elements
	
	@classmethod
	def for_player_as_xml(self, playerID):
		return self.many_to_xml(self.for_player(playerID))

Model = declarative_base(cls=ModelBase, name='Model')
Model.query = session.query_property()

def find(cls, feild, value):
	return session.execute(select(cls).where(getattr(cls, feild) == value)).all()

def find_one(cls, feild, value):
	return session.execute(select(cls).where(getattr(cls, feild) == value)).one()[0]

def exists(cls, feild, value):
	return session.query(cls).filter(getattr(cls, feild) == value).one_or_none() != None

def add(obj):
	session.add(obj)

def delete(obj):
	session.delete(obj)

def commit():
	session.commit()

def create_tables():
	Model.metadata.create_all(engine)
