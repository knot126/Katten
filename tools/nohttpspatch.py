#!/usr/bin/env python3
import io
import pathlib
import sys
import json

class MachOFormatError(Exception):
	pass

class Stream:
	"""
	Basic file stream wrapper
	"""
	
	def __init__(self, contents):
		self.f = io.BytesIO(contents)
	
	def setAddrSize(self, size):
		self.addr_size = size
	
	def getAddrSize(self):
		return self.addr_size
	
	def read(self, count):
		return self.f.read(count)
	
	def write(self, data):
		self.f.write(data)
	
	def getPos(self):
		return self.f.tell()
	
	def setPos(self, pos):
		self.f.seek(pos, 0)
	
	def skip(self, count):
		self.f.seek(count, 1)
	
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
		return int.from_bytes(self.read(1), 'little')
	
	def readUInt16(self):
		return int.from_bytes(self.read(2), 'little')
	
	def readUInt32(self):
		return int.from_bytes(self.read(4), 'little')
	
	def readUInt64(self):
		return int.from_bytes(self.read(8), 'little')
	
	def readAddr(self):
		return int.from_bytes(self.read(self.addr_size), 'little')
	
	def readFixedString(self, size):
		"""
		Read a fixed size string
		"""
		
		return self.read(size).rstrip(b'\x00').decode('utf-8')

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
		
		self.sections = []
		for i in range(self.section_count):
			self.sections.append(MachOSection(f))
	
	def getSection(self, name):
		for s in self.sections:
			if s.name == name:
				return s
		
		return None

class MachO:
	def __init__(self, content):
		f = Stream(content)
		self.segments = []
		
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
				
				case _:
					print(f"Skip LC type={lc_type} size={lc_size}")
					f.skip(lc_size - 8)
	
	def getSegment(self, name):
		for s in self.segments:
			if s.name == name:
				return s
		
		return None

def split_fat(content):
	"""
	Split a fat binary into multipule binaries, or return a list of one binary
	if this is a valid single MachO
	"""
	
	if content.startswith(b"\xce\xfa\xed\xfe"):
		return [content]
	
	f = Stream(content)
	
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
	binaries = split_fat(pathlib.Path(sys.argv[1]).read_bytes())
	
	for b in binaries:
		b = MachO(b)
		__cstring = b.getSegment("__TEXT").getSection("__cstring")
		__cfstring = b.getSegment("__DATA").getSection("__cfstring")
		
		addrOfHttps = __cstring.findAddress(b"https\x00")
		offsetToHttps = __cstring.findOffset(b"https\x00")
		print(f"address = {hex(addrOfHttps)}   offset = {hex(offsetToHttps)}")
		
		bytesToUpdate = int32ToBytes(addrOfHttps) + int32ToBytes(5)
		offsetToLength = __cfstring.findAddress(bytesToUpdate) + 4
		print(f"offset to length of string = {hex(offsetToLength)}")
