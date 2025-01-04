#!/usr/bin/env python3
import sys
from pathlib import Path
from nohttpspatch import Stream

class FatWriter:
	def __init__(self):
		self.binaries = []
	
	def append(self, content):
		"""
		Add a fat binary
		"""
		
		s = Stream(content)
		
		if s.readUInt32() != 0xfeedface:
			raise Exception("Not a 32bit MachO binary")
		
		t = s.readUInt32()
		st = s.readUInt32()
		
		self.binaries.append({"type": t, "subtype": st, "content": content})
	
	def finalise(self, align=12):
		"""
		Write a 32-bit fat binary
		"""
		
		s = Stream(b"")
		s.setEndian('big')
		s.writeUInt32(0xcafebabe)
		s.writeUInt32(len(self.binaries))
		
		for b in self.binaries:
			s.writeUInt32(b["type"])
			s.writeUInt32(b["subtype"])
			s.writeUInt32(0) # temp value
			s.writeUInt32(len(b["content"]))
			s.writeUInt32(align)
		
		# Write binaries
		for i in range(len(self.binaries)):
			b = self.binaries[i]
			
			# Write bytes to align it
			s.write(b'\x00' * ((2 ** align) - (s.getPos() % (2 ** align))))
			
			# Set position in header
			pos = s.getPos()
			s.writeUInt32To(8 + 20 * i + 8, pos)
			
			# Write contents
			s.write(b["content"])
		
		return s.getContent()

def main():
	binaries = sys.argv[1:-1]
	
	fat = FatWriter()
	
	for b in binaries:
		fat.append(Path(b).read_bytes())
	
	Path(sys.argv[-1]).write_bytes(fat.finalise())

if __name__ == "__main__":
	main()
