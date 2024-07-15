"""
Essentially, this is a database module.

This provides a standard interface for objects that will be stored in the
database and makes them a lot nicer to work with.
"""

from config import *
import sys
import pymongo

client = pymongo.mongo_client.MongoClient(PLUS_MONGO_URI)

# Test to make sure the server is actually there
try:
	client.admin.command('ping')
except pymongo.errors.ConnectionFailure:
	print(f"The Plus server could not connect to MongoDB at '{PLUS_MONGO_URI}'.\nPlease make sure that MongoDB is running and accessable to the Plus server.")
	sys.exit(1)

class Object: pass

def get_collection(classname):
	return client.get_database(PLUS_DEFAULT_DB).get_collection(classname)

class Persistent:
	"""
	Base class for all persistent objects in the Plus server.
	"""
	
	version = 0
	
	def __init__(self):
		"""
		Default constructor for a persistent object. Just creates an empty object.
		"""
		
		pass
	
	@classmethod
	def create(self, id = None):
		"""
		Same as non-classmethod create() except it automatically makes a target
		object.
		"""
		
		obj = self()
		obj.create(id)
		return obj
	
	@classmethod
	def load(self, id):
		"""
		Same as non-classmethod load() except it automatically makes a target
		object.
		"""
		
		obj = self()
		obj.load(id)
		return obj
	
	@classmethod
	def lookup(self, filter):
		"""
		Load an object with the given attributes
		"""
		
		obj = self()
		obj.load(None, filter)
		return obj
	
	@classmethod
	def make_id(self):
		"""
		Make a new identifier which is definitely unique. The default
		implementation is an incremental counter starting from 1.
		"""
		
		return (get_collection(self.__name__).count_documents({}) + 1)
	
	@classmethod
	def exists(self, id):
		"""
		Return true if an entry with the given id exists, false if not.
		"""
		
		coll = get_collection(self.__name__)
		
		return (coll.find_one({"_id": id}) != None)
	
	def create(self, id = None):
		"""
		Create a new, non-existing object.
		"""
		
		# Init object data structure
		if (id == None):
			id = self.get_class().make_id()
		
		self._id = id
		self._ver = self.get_class().version
		
		if (self.get_class().exists(id)):
			raise Exception("Object with id already exists!")
		
		# User init function
		self.on_init()
		
		# Save initial object to DB
		coll = get_collection(self.get_class_name())
		
		coll.insert_one(self.__dict__)
	
	def load(self, id, filter = None):
		"""
		Load an existing persistent object into this object
		"""
		
		if (id and filter == None):
			filter = {"_id": id}
		
		# Load data from DB
		coll = get_collection(self.get_class_name())
		
		result = coll.find_one(filter)
		
		if (result == None):
			raise Exception("Object does not yet exist!")
		
		self.__dict__ = dict(result)
		
		# User load function
		self.on_load()
		
		# Check for data structure upgrades
		if (self.get_class().version > self.get_version()):
			self.on_update(self._ver)
	
	def save(self):
		"""
		Save the persistent object to the database
		"""
		
		# Call user pre-save function
		self.on_save()
		
		# Save data
		coll = get_collection(self.get_class_name())
		
		coll.find_one_and_replace({"_id": self._id}, self.__dict__)
	
	def delete(self):
		"""
		Remove the persistent object from the database
		"""
		
		# Call user delete function
		self.on_delete()
		
		# Delete object from DB
		coll = get_collection(self.get_class_name())
		
		coll.delete_one({"_id": self._id})
	
	def set_version(self, ver):
		"""
		Set the version of the current object
		"""
		
		self._ver = ver
	
	def get_version(self):
		"""
		Get the version of the current object
		"""
		
		return self._ver
	
	def get_class(self):
		"""
		Get the class of this object
		"""
		
		return self.__class__
	
	def get_class_name(self):
		"""
		Get this object's class name
		"""
		
		return self.get_class().__name__
	
	def on_init(self):
		"""
		Called when the object is first created in the database.
		"""
		
		pass
	
	def on_load(self):
		"""
		Called when the object is loaded from the database. Note that this does
		not include 
		"""
		
		pass
	
	def on_save(self):
		"""
		Called before the object is saved to the database.
		"""
		
		pass
	
	def on_update(self, prev_version):
		"""
		Called after on_load() when an object with an outdated structure is
		detected.
		"""
		
		pass
	
	def on_delete(self):
		"""
		Called when the object is deleted from the database.
		"""
		
		pass
