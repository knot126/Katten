from flask import Flask, Response, request

app = Flask(__name__)

@app.get("/touchpet/gamedata/get_dlc.php")
def get_dlc_php():
	return ""

@app.get("/touchpet/gamedata/messages.php")
def messages_php():
	return ""

@app.get("/touchpet/gamedata/rewards.php")
def rewards_php():
	return ""

@app.post("/touchpet/")
def touchpet_index():
	cmd = request.form["cmd"]
	
	match cmd:
		case "player":
			return Response("<players><player></player></players>", mimetype="text/xml")
		
		case "pets":
			return Response("<pets></pets>", mimetype="text/xml")
