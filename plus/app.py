#!/usr/bin/env python3

from flask import Flask
from sys import argv, exit
import database
import routes

import user
import game
import session
import flags
import asset
import app_data
import system_message
import badge
import misc
import leaderboards
# import buddy

if "--initial-setup" in argv:
	database.create_tables()
	exit(0)

app = Flask(__name__)
app.register_blueprint(asset.bp)
app.register_blueprint(flags.bp)
app.register_blueprint(user.bp)
app.register_blueprint(game.bp)
app.register_blueprint(session.bp)
app.register_blueprint(badge.bp)
app.register_blueprint(app_data.bp)
app.register_blueprint(misc.bp)
app.register_blueprint(leaderboards.bp)
# app.register_blueprint(buddy.bp)
