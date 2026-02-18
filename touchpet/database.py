from sys import argv, exit
from config import *
from pathlib import Path
from sqlalchemy import create_engine, Table, Boolean, Integer, String, Unicode, ForeignKey, select, text, desc
from sqlalchemy.schema import Column
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from sqlalchemy.exc import NoResultFound
from xml.etree.ElementTree import Element, tostring
import re

__all__ = [
	"Table", "Boolean", "Integer", "String", "Unicode", "ForeignKey", "select",
	"text", "desc", "Column", "relationship", "NoResultFound", "Model"
]

if len(argv) < 2:
	print("Missing first argument: should be cats, dogs2, or dogs")
	exit(127)

TP_DATABASE_URI = TP_DATABASE_URI if TP_DATABASE_URI else ("sqlite:///" + str(Path(TP_DATA_PATH).expanduser()) + argv[1] + ".db")

engine = create_engine(TP_DATABASE_URI)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class ModelBase:
	def to_xml(self):
		root = Element(self.__class__.__name__)
		
		for col in dir(self.__class__):
			if type(getattr(self.__class__, col)) == Column:
				e = Element(col)
				e.text = str(getattr(self, col))
				root.append(e)
		
		return root
	
	def to_inline_xml(self):
		element = Element(self.__class__.__name__)
		
		for col in dir(self.__class__):
			if type(getattr(self.__class__, col)) == Column:
				element.set(col, str(getattr(self, col)))
		
		return element
	
	@classmethod
	def get(self, id):
		return session.query(self).get(id)

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

def commit():
	session.commit()

def create_tables():
	Model.metadata.create_all(engine)
