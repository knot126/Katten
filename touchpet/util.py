import urllib.request
import urllib.parse
import json
from time import time as unixtime

def post(url, data):
	req = urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode('utf-8'), method='POST'))
	result = json.loads(req.read().decode('utf-8'))
	return result

def time():
	return int(unixtime())

__all__ = ["post", "time"]
