"""
Touch pet server config
"""

# URI for MongoDB
TP_MONGO_URI = "mongodb://localhost:27017"

# Control which game appnames maps to which database. For reasons of history, PetCat
# just gets mapped to the generic "TouchPets" db name.
TP_DATABASE_MAPS = {
	"PetCat": "TouchPets",
	"PetDog2": "PetDog2",
	"PetDog": "PetDog",
}

# Appname to use if none could be found via the user agent
TP_DEFAULT_APPNAME = "PetCat"

# URI of the Plus+ server
PLUS_SERVER = "localhost:5100"

__all__ = list(globals().keys())
