from plistlib import UID
import json

data = {'$top': {'Pet': UID(1)}, '$objects': ['$null', {'playdates': UID(4), 'timeadopted': UID(6), 'relationships': UID(2), 'excludedFromDisk': UID(6), 'playerID': UID(7), 'updateTime': UID(10), 'ready': UID(5), 'petname': UID(8), 'gender': UID(5), 'propertiesByCategory': UID(12), '$class': UID(61), 'breedID': UID(6), 'petID': UID(9), 'uuidsToPost': UID(0)}, {'NS.objects': [], '$class': UID(3)}, {'$classes': ['NSMutableArray', 'NSArray', 'NSObject'], '$classname': 'NSMutableArray'}, {'NS.objects': [], '$class': UID(3)}, 1, 0, 5, 'Maverick', 3, {'$class': UID(11), 'NS.time': 781894995.958176}, {'$classes': ['NSDate', 'NSObject'], '$classname': 'NSDate'}, {'NS.objects': [UID(19), UID(31), UID(37), UID(56), UID(58), UID(59)], 'NS.keys': [UID(13), UID(14), UID(15), UID(16), UID(17), UID(18)], '$class': UID(30)}, 'category_8', 'category_2', 'category_7', 'category_5', 'category_3', 'category_1', {'NS.objects': [UID(25), UID(26), UID(27), UID(28), UID(29)], 'NS.keys': [UID(20), UID(21), UID(22), UID(23), UID(24)], '$class': UID(30)}, 'property_8', 'property_10', 'property_9', 'property_7', 'property_5', 100, 100, 100, 100, 100, {'$classes': ['NSMutableDictionary', 'NSDictionary', 'NSObject'], '$classname': 'NSMutableDictionary'}, {'NS.objects': [UID(6), UID(6), UID(36), UID(6)], 'NS.keys': [UID(32), UID(33), UID(34), UID(35)], '$class': UID(30)}, 'property_1', 'property_2', 'property_0', 'property_3', 2, {'NS.objects': [UID(45), UID(46), UID(6), UID(47), UID(48), UID(49), UID(6), UID(50), UID(6), UID(51), UID(52), UID(6), UID(53), UID(6), UID(54), UID(55)], 'NS.keys': [UID(35), UID(24), UID(23), UID(34), UID(21), UID(22), UID(38), UID(33), UID(39), UID(40), UID(41), UID(42), UID(43), UID(44), UID(20), UID(32)], '$class': UID(30)}, 'property_11', 'property_12', 'property_4', 'property_13', 'property_6', 'property_14', 'property_15', 30, 99, 94, 100, 25, 46, 44, 72, 34, 99, 18, {'NS.objects': [UID(57), UID(57), UID(57), UID(57), UID(57), UID(57), UID(57), UID(57), UID(57)], 'NS.keys': [UID(33), UID(20), UID(32), UID(23), UID(34), UID(42), UID(24), UID(40), UID(35)], '$class': UID(30)}, -1, {'NS.objects': [UID(6), UID(6), UID(6), UID(9), UID(9), UID(6), UID(36)], 'NS.keys': [UID(33), UID(32), UID(34), UID(42), UID(24), UID(40), UID(35)], '$class': UID(30)}, {'NS.objects': [UID(7), UID(7), UID(5), UID(5), UID(60)], 'NS.keys': [UID(32), UID(42), UID(33), UID(34), UID(24)], '$class': UID(30)}, 1760202191, {'$classes': ['SEPetModel', 'SERemoteModel', 'NSObject'], '$classname': 'SEPetModel'}], '$version': 100000, '$archiver': 'NSKeyedArchiver'}

def parse(objects, object):
	obj_type = type(object)
	
	if obj_type == UID:
		if object == UID(0): return None
		return parse(objects, objects[object.data])
	elif obj_type == list:
		return [parse(objects, x) for x in object]
	elif obj_type == dict:
		if '$class' in object:
			if 'NS.keys' in object:
				keys = object['NS.keys']
				values = object['NS.objects']
				return {parse(objects, keys[i]): parse(objects, values[i]) for i in range(len(keys))}
			elif 'NS.objects' in object:
				return [parse(objects, d) for d in object['NS.objects']]
			elif 'NS.time' in object:
				return object['NS.time']
			else:
				return {k: parse(objects, v) for k, v in object.items() if k != '$class'}
		else:
			return {}
	else:
		return object

def parse_from_root(root):
	top = list(root['$top'].values())[0]
	objs = root['$objects']
	return parse(objs, top)

#TODO else : return object

print( json.dumps(parse_from_root(data), indent=4) )
