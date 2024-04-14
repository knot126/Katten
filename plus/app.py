from flask import Flask, request, g, make_response, url_for
from pathlib import Path
import os
import os.path

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

require_dir("core")
require_dir("routes")
