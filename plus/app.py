#!/usr/bin/env python3

from flask import Flask
from sys import argv, exit
import database
import routes

import user
import game
import flags
import asset
import app_data

if "--initial-setup" in argv:
	database.create_tables()
	exit(0)

app = Flask(__name__)
app.register_blueprint(routes.bp)
app.register_blueprint(flags.bp)
app.register_blueprint(asset.bp)
