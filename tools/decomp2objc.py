#!/usr/bin/env python3
"""
Try to automatically clean up a ghidra decompliation to be closer to Objective-C
"""

import sys
from pathlib import Path
import csplit

def getargs(snippet):
	i = snippet.index('(') + 1
	bal = 1
	args = []
	
	lastarg = i
	last = None
	
	while bal:
		if snippet[i] == '(':
			i += 1
			bal += 1
			continue
		if snippet[i] == ')':
			bal -= 1
			if bal == 0:
				args.append(snippet[lastarg:i])
				last = i
			i += 1
			continue
		if bal == 1 and snippet[i] == ',':
			args.append(snippet[lastarg:i])
			lastarg = i+1
		
		i += 1
	
	return args, last

def cleansuffix(objname):
	return objname.removeprefix("&objc::class_t::").removeprefix("&_OBJC_CLASS_$_")

def cleanarg(argstr):
	if argstr.startswith("&cf_"):
		return '@"' + argstr[4:] + '"'
	else:
		return argstr

def cleanup(code):
	code = csplit.csplit(code)
	new = []
	
	i = 0
	
	while i < len(code):
		if code[i] == '_objc_msgSend':
			args, inc = getargs(code[i+1:])
			i += inc + 2
			
			if len(args) < 2:
				new.append('[???]')
				continue
			
			self = ''.join(args[0])
			sel = ''.join(args[1])[1:-1]
			
			if len(args) == 2:
				new.append(f"[{cleansuffix(self)} {sel}]")
			else:
				selparts = sel.split(':')[:-1]
				print(selparts)
				s = ""
				
				for j in range(2, len(args)):
					argstr = cleanarg(''.join(args[j]).strip())
					
					if j >= len(selparts)+2:
						s += f", {argstr}"
					else:
						s += f" {selparts[j-2]}: {argstr}"
				
				new.append(f"[{cleansuffix(self)}{s}]")
		else:
			new.append(code[i])
			i += 1
	
	return ''.join(new)

def main():
	print(cleanup(Path(sys.argv[1]).read_text()))

if __name__ == "__main__":
	main()
