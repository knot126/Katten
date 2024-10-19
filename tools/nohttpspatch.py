#!/usr/bin/env python3
import io
import pathlib
import sys
import json
import hashlib

def sha1(b):
	return hashlib.sha1(b).digest()

def sha256(b):
	return hashlib.sha256(b).digest()

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
		See:
		- https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/kern/cs_blobs.h
		- https://github.com/qyang-nj/llios/blob/main/macho_parser/docs/LC_CODE_SIGNATURE.md
		- https://github.com/xerub/ldid/blob/master/ldid2.cpp#L1240
		- https://alfiecg.uk/2024/01/06/Ad-hoc-signing.html
		
		We only really need the basic header, we just want to regenerate the
		hashes and nothing really advanced.
		
		Expcets big endian mode.
		"""
		
		self.filepos = f.getPos()
		self.magic = f.readUInt32()
		self.length = f.readUInt32()
		self.version = f.readUInt32()
		self.flags = f.readUInt32()
		self.hash_offset = f.readUInt32() # Offset to hash at index *zero*, skips negatives!
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
		f.setPos(self.filepos + self.identifier_offset)
		self.identifier = f.readTerminatedString()
		
		# Read hashes
		self.slots = []
		f.setPos(self.filepos + self.hash_offset - (self.hash_size * self.num_special_slots))
		for i in range(self.num_special_slots + self.num_code_slots):
			self.slots.append(f.read(self.hash_size))
		# print(hex(f.getPos()))
	
	def printInfo(self):
		print(self.__dict__)

class MachOCodeSignBlob:
	"""
	Any unknown code sign blob becomes this. Expects big endian mode.
	"""
	
	def __init__(self, f, type, offset):
		self.type = type
		self.offset = offset
		self.filepos = f.getPos()
		self.magic = f.readUInt32()
		self.length = f.readUInt32()
		self.content = f.read(self.length - 8)
	
	def printInfo(self):
		print(f"  - {hex(self.magic)} {hex(self.length)} {self.content}")

class MachOCodeSignSuperblob:
	"""
	The code signing super blob and everything in it
	"""
	
	def __init__(self, f, cs_offset, cs_size):
		self.code_dirs = []
		self.blobs = []
		self.offset = cs_offset # offset from start of file
		self.size = cs_size # size of code signing blob
		
		f.push()
		f.setPos(self.offset)
		f.setEndian('big') # integers are big endian here for some reason
		
		self.magic = f.readUInt32()
		self.length = f.readUInt32()
		self.count = f.readUInt32()
		
		print(f"magic={hex(self.magic)} length={hex(self.length)} count={hex(self.count)}")
		
		for i in range(self.count):
			type = f.readUInt32()
			blob_offset = f.readUInt32()
			blob_filepos = self.offset + blob_offset
			print(f"type={type} offset-from-file={blob_filepos}")
			
			# Add raw blob data
			f.push()
			f.setPos(blob_filepos)
			self.blobs.append(MachOCodeSignBlob(f, type, blob_offset))
			self.blobs[-1].printInfo()
			f.pop()
			
			# Code directory blobs also get structured data
			if (type == 0 or 0x1000 <= type < 0x1005):
				f.push()
				f.setPos(blob_filepos)
				self.code_dirs.append(MachOCodeDirectory(f))
				f.pop()
		
		f.setEndian('little')
		f.pop()

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
				
				case 0x1d:
					# Code signature
					self.cs_offset = f.readUInt32() # Offset from __LINKEDIT section
					self.cs_size = f.readUInt32()
				
				case _:
					# print(f"Skip LC type={hex(lc_type)} size={hex(lc_size)}")
					f.skip(lc_size - 8)
		
		self.cs_superblob = MachOCodeSignSuperblob(f, self.cs_offset, self.cs_size)
	
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

def fakesign_recompute_hashes(binary_contents, limit, pagesize=12, algorithm=1):
	"""
	Recompute the non-special CDHashes given the binary's data and the number of
	hashes to compute.
	"""
	
	pagesize = 2 ** pagesize
	hashes = []
	current = 0
	
	while current < limit:
		data = binary_contents[current:current + min(limit - current, pagesize)]
		
		match algorithm:
			case 1:
				hashes.append(sha1(data))
			case 2:
				hashes.append(sha256(data))
			case _:
				raise ValueError(f"Unsupported or invalid algorithm: {algorithm}")
		
		current += pagesize
	
	return hashes

def fakesign(content):
	"""
	Return a fakesigned version of the Mach-O given the contents. This does a
	job similar to ldid with the -s option.
	"""
	
	binary_info = MachO(content)
	new_binary = Stream(content)
	
	print("Update CDHashes...")
	
	for cd in binary_info.cs_superblob.code_dirs:
		print(f"Recomptue hashes for code directory at {hex(cd.filepos)} (code_limit {hex(cd.code_limit)} page_size {hex(cd.page_size)} hash_type {hex(cd.hash_type)})...")
		
		new_hashes = fakesign_recompute_hashes(content, cd.code_limit, cd.page_size, cd.hash_type)
		
		if (len(new_hashes) != cd.num_code_slots):
			print(f"Warning: codedir hash array lengths are not equal ({len(new_hashes)} != {cd.num_code_slots}) !!")
		
		for i in range(len(new_hashes)):
			if (new_hashes[i] != cd.slots[cd.num_special_slots + i]):
				print(f"Different hash at index {i}: {new_hashes[i]} != {cd.slots[cd.num_special_slots + i]}")
		
		# Go to where the hashes are and write them
		print("Write recomputed hashes")
		new_binary.setPos(cd.filepos + cd.hash_offset)
		new_binary.write(b"".join(new_hashes))
	
	print(f"Find and remove CMS digital signature blob(s)...")
	
	# Get info for new superblob
	new_sb = bytearray() # New SB content
	new_sb_count = 0 # New count
	
	for blob in binary_info.cs_superblob.blobs:
		if blob.type != 0x10000:
			new_sb += int32ToBytes(blob.type, 'big')
			new_sb += int32ToBytes(blob.offset, 'big')
			new_sb_count += 1
	
	# Add new super blob header
	new_sb = b"\xfa\xde\x0c\xc0" + int32ToBytes(binary_info.cs_superblob.length, 'big') + int32ToBytes(new_sb_count, 'big') + new_sb
	
	print(f"!! New super blob: {new_sb}")
	
	# Seek to start of blob indexes and write it
	new_binary.setPos(binary_info.cs_superblob.offset)
	new_binary.write(new_sb)
	
	return new_binary.getContent()

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

def int32ToBytes(value, endian='little'):
	return value.to_bytes(4, endian)

def main():
	infile = sys.argv[1]
	binaries = split_fat(pathlib.Path(infile).read_bytes())
	
	for b in binaries:
# 		p = Stream(b)
# 		b = MachO(b)
# 		
# 		print(f"Patching a binary (for {b.getArchName()})...")
# 		__cstring = b.getSegment("__TEXT").getSection("__cstring")
# 		__cfstring = b.getSegment("__DATA").getSection("__cfstring")
# 		__LINKEDIT = b.getSegment("__LINKEDIT")
# 		print(f"Code signing data at __LINKEDIT+{hex(b.cs_offset)} (length={hex(b.cs_size)})")
# 		
# 		addrOfHttps = __cstring.findAddress(b"https\x00")
# 		offsetToHttps = __cstring.findOffset(b"https\x00")
# 		print(f"address = {hex(addrOfHttps)}   offset = {hex(offsetToHttps)}")
# 		
# 		bytesToUpdate = int32ToBytes(addrOfHttps) + int32ToBytes(5)
# 		offsetToLength = __cfstring.findAddress(bytesToUpdate) + 4
# 		print(f"offset to length of string = {hex(offsetToLength)}")
# 		
# 		p.patch(offsetToHttps, b"http\x00")
# 		p.patch(offsetToLength, int32ToBytes(4))
# 		pathlib.Path(f"{infile}-patched-{b.getArchName()}").write_bytes(p.getContent())
		
		fakesign(b)
		
		pass
	
	print(f"Done!")

if __name__ == "__main__":
	main()
