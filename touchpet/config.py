"""
Touch pet server config
"""

from os import environ

TP_DATABASE_URI = environ.get("TP_DATABASE_URI", None)
TP_DATA_PATH = environ.get("TP_DATA_PATH", "~/.katten/touchpets/")

# URI of the Plus+ server
TP_PLUS_SERVER = environ.get("TP_PLUS_SERVER", "localhost:5100")

# Name of the app. One of cats, dogs2, dogs
TP_APPNAME = environ.get("TP_APPNAME", "cats")

print(f"Hosting server for {TP_APPNAME}")
assert(TP_APPNAME in {"cats", "dogs2", "dogs"})

__all__ = [
	"TP_DATABASE_URI",
	"TP_DATA_PATH",
	"TP_PLUS_SERVER",
	"TP_APPNAME",
]
