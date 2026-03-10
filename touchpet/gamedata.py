from flask import Blueprint

# ===============================
#           Game Data
# ===============================
gamedata = Blueprint("gamedata", __name__)

@gamedata.get("/touchpet/gamedata/get_dlc.php")
def get_dlc_php():
	return ""

@gamedata.get("/touchpet/gamedata/messages.php")
def messages_php():
	return ""

@gamedata.get("/touchpet/gamedata/rewards.php")
def rewards_php():
	return ""

@gamedata.get("/touchpet/gamedata/getpid.php")
def getpid_php():
	return ""

@gamedata.get("/touchpet/gamedata/petmaster.php")
def petmaster_php():
	return "<h1><span style=\"color: red;\">Katten Server does not support microtransactions.</span></h1>"
