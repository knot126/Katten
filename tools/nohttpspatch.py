#!/usr/bin/env python3
import io
import pathlib
import sys
import json
import hashlib

class MachOFormatError(Exception):
	pass

class Stream:
	"""
	Basic file stream wrapper with endian control and a stack for pushing/poping
	the current position.
	"""
	
	def __init__(self, contents):
		self.f = io.BytesIO(contents)
		self.endian = 'little'
		self.posStack = []
	
	def setAddrSize(self, size):
		self.addr_size = size
	
	def setEndian(self, endian):
		self.endian = endian
	
	def getAddrSize(self):
		return self.addr_size
	
	def getContent(self):
		return self.f.getvalue()
	
	def read(self, count):
		return self.f.read(count)
	
	def write(self, data):
		self.f.write(data)
	
	def skip(self, count):
		self.f.seek(count, 1)
	
	def getPos(self):
		return self.f.tell()
	
	def setPos(self, pos):
		self.f.seek(pos, 0)
	
	def readFrom(self, pos, count):
		"""
		Read a block from a specific position of the stream
		"""
		old_pos = self.getPos()
		self.setPos(pos)
		data = self.read(count)
		self.setPos(old_pos)
		return data
	
	def patch(self, pos, content):
		"""
		Write a patch to the stream
		"""
		old_pos = self.getPos()
		self.setPos(pos)
		self.write(content)
		self.setPos(old_pos)
	
	def readUInt8(self):
		return int.from_bytes(self.read(1), self.endian)
	
	def readUInt16(self):
		return int.from_bytes(self.read(2), self.endian)
	
	def readUInt32(self):
		return int.from_bytes(self.read(4), self.endian)
	
	def readUInt64(self):
		return int.from_bytes(self.read(8), self.endian)
	
	def readAddr(self):
		return int.from_bytes(self.read(self.addr_size), self.endian)
	
	def readFixedString(self, size):
		"""
		Read a fixed size string
		"""
		
		return self.read(size).rstrip(b'\x00').decode('utf-8')
	
	def readTerminatedString(self):
		s = b""
		
		while True:
			c = self.read(1)
			if c == b"\x00": break
			s += c
		
		return s.decode('utf-8')
	
	def writeUInt8(self, value):
		self.write(value.to_bytes(1, self.endian))
	
	def writeUInt16(self, value):
		self.write(value.to_bytes(2, self.endian))
	
	def writeUInt32(self, value):
		self.write(value.to_bytes(4, self.endian))
	
	def push(self):
		self.posStack.append(self.getPos())
	
	def pop(self):
		self.setPos(self.posStack.pop())

class MachOSection:
	def __init__(self, f):
		# Read section from f
		self.name = f.readFixedString(16)
		self.segment_name = f.readFixedString(16)
		self.address = f.readUInt32()
		self.size = f.readUInt32()
		self.offset = f.readUInt32()
		self.alignment = f.readUInt32()
		self.reloc_offset = f.readUInt32()
		self.reloc_count = f.readUInt32()
		self.flag = f.readUInt32()
		self.content = f.readFrom(self.offset, self.size)
		# reserved feilds
		f.readUInt32()
		f.readUInt32()
	
	def find(self, content):
		"""
		Find the offset to the first occurance of `content` relative to the section
		"""
		
		r = self.content.find(content)
		
		if r == -1:
			raise ValueError(f"The content {content} was not found in segment={self.segment_name} section={self.name}")
		
		return r
	
	def findAddress(self, content):
		"""
		Find address of the first occurance of content
		"""
		
		return self.address + self.find(content)
	
	def findOffset(self, content):
		"""
		Find the offset of the first occurence of content relative to the mach-o
		file
		"""
		
		return self.offset + self.find(content)
	
	def getContent(self):
		return self.content

class MachOSegment:
	def __init__(self, f):
		# Read segment from start of load command (after LC header)
		self.name = f.readFixedString(16)
		self.address = f.readUInt32()
		self.loaded_size = f.readUInt32()
		self.offset = f.readUInt32()
		self.size = f.readUInt32()
		self.vm_max_protections = f.readUInt32()
		self.vm_flags = f.readUInt32()
		self.section_count = f.readUInt32()
		self.flags = f.readUInt32()
		self.content = f.readFrom(self.offset, self.size)
		
		self.sections = []
		for i in range(self.section_count):
			self.sections.append(MachOSection(f))
	
	def getSection(self, name):
		for s in self.sections:
			if s.name == name:
				return s
		
		return None

class MachOCodeDirectory:
	def __init__(self, f):
		"""
		See https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/kern/cs_blobs.h
		
		We only really need the basic header, we just want to regenerate the
		hashes and nothing really advanced.
		"""
		
		start = f.getPos()
		magic = f.readUInt32()
		self.length = f.readUInt32()
		self.version = f.readUInt32()
		self.flags = f.readUInt32()
		self.hash_offset = f.readUInt32()
		self.identifier_offset = f.readUInt32()
		self.num_special_slots = f.readUInt32()
		self.num_code_slots = f.readUInt32()
		self.code_limit = f.readUInt32() # End of hashed pages
		self.hash_size = f.readUInt8() # Size of each hash
		self.hash_type = f.readUInt8() # Hash algorithm
		self.platform = f.readUInt8()
		self.page_size = f.readUInt8()
		f.readUInt32() # unused
		
		# Read identifier string
		f.setPos(start + self.identifier_offset)
		self.identifier = f.readTerminatedString()
		
		# Read hashes
		self.slots = []
		f.setPos(start + self.hash_offset - (self.hash_size * self.num_special_slots))
		for i in range(self.num_special_slots + self.num_code_slots):
			self.slots.append(f.read(self.hash_size))
		print(hex(f.getPos()))
	
	def printInfo(self):
		print(self.__dict__)

class MachO:
	def __init__(self, content):
		f = Stream(content)
		self.segments = []
		self.code_dirs = []
		
		magic = f.readUInt32()
		
		if magic == 0xfeedface:
			pass
		elif magic == 0xfeedfacf:
			raise MachOFormatError("64-bit MachO's are not supported")
		else:
			raise MachOFormatError("Invalid MachO magic number")
		
		self.cpu_type = f.readUInt32()
		self.cpu_subtype = f.readUInt32()
		self.file_type = f.readUInt32()
		lc_count = f.readUInt32()
		lc_total_size = f.readUInt32()
		self.flags = f.readUInt32()
		
		for i in range(lc_count):
			lc_type = f.readUInt32()
			lc_size = f.readUInt32()
			
			match lc_type:
				case 0x1:
					# Segment
					self.segments.append(MachOSegment(f))
				
				case 0x1d:
					# Code signature
					self.cs_offset = f.readUInt32() # Offset from __LINKEDIT section
					self.cs_size = f.readUInt32()
				
				case _:
					# print(f"Skip LC type={hex(lc_type)} size={hex(lc_size)}")
					f.skip(lc_size - 8)
		
		self._parseCDHashData(f)
	
	def _parseCDHashData(self, f):
		f.push()
		f.setPos(self.cs_offset)
		f.setEndian('big')
		
		sb_magic = f.readUInt32()
		sb_length = f.readUInt32()
		sb_count = f.readUInt32()
		
		print(f"magic={hex(sb_magic)} length={hex(sb_length)} count={hex(sb_count)}")
		
		for i in range(sb_count):
			type = f.readUInt32()
			offset = f.readUInt32()
			blob_offset = self.cs_offset + offset
			print(f"type={type} offset-from-file={blob_offset}")
			
			if (type == 0):
				f.push()
				f.setPos(blob_offset)
				self.code_dirs.append(MachOCodeDirectory(f))
				f.pop()
		
		f.setEndian('little')
		f.pop()
	
	def getSegment(self, name):
		for s in self.segments:
			if s.name == name:
				return s
		
		return None
	
	def getArchName(self):
		try:
			return {0xC: {0x6: "armv6", 0x9: "armv7", 0xA: "armv7f", 0xD: "armv8"}}[self.cpu_type][self.cpu_subtype]
		except:
			return f"{self.cpu_type}_{self.cpu_subtype}"

def split_fat(content):
	"""
	Split a fat binary into multipule binaries, or return a list of one binary
	if this is a valid single MachO
	"""
	
	if content.startswith(b"\xce\xfa\xed\xfe"):
		return [content]
	
	f = Stream(content)
	f.setEndian('big')
	
	if (f.read(4) != b"\xca\xfe\xba\xbe"):
		raise MachOFormatError("Invalid fat binary")
	
	count = f.readUInt32()
	binaries = []
	
	for i in range(count):
		cpu_type = f.readUInt32()
		cpu_subtype = f.readUInt32()
		offset = f.readUInt32()
		size = f.readUInt32()
		alignment = f.readUInt32()
		binaries.append(f.readFrom(offset, size))
	
	return binaries

def int32ToBytes(value):
	return value.to_bytes(4, 'little')

if __name__ == "__main__":
	infile = sys.argv[1]
	binaries = split_fat(pathlib.Path(infile).read_bytes())
	
	for b in binaries:
		p = Stream(b)
		b = MachO(b)
		print(f"Patching a binary (for {b.getArchName()})...")
		__cstring = b.getSegment("__TEXT").getSection("__cstring")
		__cfstring = b.getSegment("__DATA").getSection("__cfstring")
		__LINKEDIT = b.getSegment("__LINKEDIT")
		print(f"Code signing data at __LINKEDIT+{hex(b.cs_offset)} (length={hex(b.cs_size)})")
		
		addrOfHttps = __cstring.findAddress(b"https\x00")
		offsetToHttps = __cstring.findOffset(b"https\x00")
		print(f"address = {hex(addrOfHttps)}   offset = {hex(offsetToHttps)}")
		
		bytesToUpdate = int32ToBytes(addrOfHttps) + int32ToBytes(5)
		offsetToLength = __cfstring.findAddress(bytesToUpdate) + 4
		print(f"offset to length of string = {hex(offsetToLength)}")
		
		p.patch(offsetToHttps, b"http\x00")
		p.patch(offsetToLength, int32ToBytes(4))
		pathlib.Path(f"{infile}-patched-{b.getArchName()}").write_bytes(p.getContent())
		
		# b.code_dirs[0].printInfo()
	
	print(f"Done!")
