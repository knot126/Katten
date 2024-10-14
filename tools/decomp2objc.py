#!/usr/bin/env python3
"""
Try to automatically clean up a ghidra decompliation to be closer to Objective-C
"""

import sys
from pathlib import Path
import re

def cleanup(code):
	# single keyword message
	code = re.sub(r'_objc_msgSend\(([&:_a-zA-Z0-9]+),"([_a-zA-Z0-9]+)"\)', r'[\1 \2]', code)
	
	# messages with arguments
	code = re.sub(r'_objc_msgSend\(([&:_a-zA-Z0-9]+),"([_a-zA-Z0-9]+:)",([&_a-zA-Z0-9]+)\)', r'[\1 \2 \3]', code)
	
	# &cf_string to "string"
	code = re.sub(r'&cf_([a-zA-Z0-9\-_]+)', r'"\1"', code)
	
	code = code.replace("&objc::class_t::", "")
	
	return code

def main():
	print(cleanup(Path(sys.argv[1]).read_text()))

if __name__ == "__main__":
	main()
