from flask import Flask, Response, request, g, make_response, url_for
from pathlib import Path
import os
import os.path

from persist import Persistent

app = Flask(__name__)

def require(path):
	"""
	Kind-of-hack to make a custom PHP-like require()
	"""
	
	exec(Path(path).read_text(), globals())

def require_dir(path):
	"""
	require() all files in a directory. Does not include subdirs.
	"""
	
	dir_contents = os.listdir(path)
	
	for f in dir_contents:
		f = path + '/' + f
		if os.path.isfile(f):
			print(f"Require {f} ...")
			require(f)

require("core/user.py")
require("core/game.py")
require_dir("routes")
