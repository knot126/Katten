"""
A really crappy HTTP router to allow running Plus+ and game servers at the same
time.
"""

from flask import Flask, Response, request
from werkzeug.routing import Rule
import urllib.request, urllib.parse, http.client
from urllib.error import HTTPError

app = Flask(__name__)

# for rule in app.url_map.iter_rules():
# 	app.url_map._rules.remove(rule)

app.url_map = type(app.url_map)()
app.url_map.add(Rule("/", endpoint = "route"))
app.url_map.add(Rule("/<path:morepath>", endpoint = "route"))
app.url_map.add(Rule("/static/<path:morepath>", endpoint = "route"))

SERVER_MAP = {
	"app.plusplus.com": "localhost:5100",
	"dogs2.ngmoco.com": "localhost:5200",
	"cats.ngmoco.com": "localhost:5200",
}

@app.endpoint("route")
def route(**unusedParams):
	url = request.url
	method = request.method
	headers = request.headers
	
	netloc_in = urllib.parse.urlparse(url).netloc
	netloc_out = SERVER_MAP.get(netloc_in, netloc_in)
	url_out = url.replace(netloc_in, netloc_out)
	
	print(f"{url} -> {url_out}")
	
	response = None
	
	try:
		response = urllib.request.urlopen(urllib.request.Request(url_out, data=request.get_data(), headers=dict(headers), method=method))
	except http.client.RemoteDisconnected:
		return Response("Router: Remote disconnected", 500)
	except HTTPError as e:
		response = e
		#return Response(f"Router: Internal error\nInput url: {url}\nOutput url: {url_out}", 500)
	
	out_status = response.status if response is not HTTPError else response.code
	out_headers = dict(response.headers)
	out_data = response.read() if response is not HTTPError else response.fp.read()
	
	return Response(out_data, out_status, out_headers)
