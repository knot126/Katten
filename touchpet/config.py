"""
Touch pet server config
"""

TP_DATABASE_URI = None
TP_DATA_PATH = "~/.katten/touchpets/"

# URI of the Plus+ server
TP_PLUS_SERVER = "localhost:5100"

# Name of the app. One of cats, dogs2, dogs
TP_APPNAME = "cats"

__all__ = [
	"TP_DATABASE_URI",
	"TP_DATA_PATH",
	"TP_PLUS_SERVER",
	"TP_APPNAME",
]
