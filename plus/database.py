"""
Database models
"""

from config import *
from flask import Blueprint
from sqlalchemy import create_engine, Boolean, Integer, String, Unicode, ForeignKey, select
from sqlalchemy.schema import Column
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

engine = create_engine(PLUS_DATABASE_URI)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()
Model = Base

bp = Blueprint(__name__, __name__)

@bp.teardown_appcontext
def shutdown_db(exception=None):
	session.remove()

def find(cls, field, value):
	return session.execute(select(cls).where(getattr(cls, field) == value)).all()

def exists(cls, field, value):
	return session.query.filter(getattr(cls, field) == value).one_or_none() != None
