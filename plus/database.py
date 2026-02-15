"""
Database models
"""

from config import *
from flask import Blueprint
from pathlib import Path
from sqlalchemy import create_engine, Table, Boolean, Integer, String, Unicode, ForeignKey, select, text, desc
from sqlalchemy.schema import Column
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from sqlalchemy.exc import NoResultFound
import re

if not PLUS_DATABASE_URI:
	PLUS_DATABASE_URI = f"sqlite:///{Path(PLUS_SQLITE_DATABASE_PATH).expanduser()}"

engine = create_engine(PLUS_DATABASE_URI)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class ModelBase:
	@classmethod
	def get(self, id):
		return session.query(self).get(id)

Model = declarative_base(cls=ModelBase, name='Model')
Model.query = session.query_property()

# bp = Blueprint(__name__, __name__)

# @bp.teardown_appcontext
def shutdown(exception=None):
	session.remove()

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
