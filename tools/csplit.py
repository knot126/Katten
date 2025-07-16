#!/usr/bin/env python3
"""
Split a string by C-style lexical tokens
"""

import re

word = re.compile(r'[a-zA-Z_][0-9a-zA-Z_]*')
number = re.compile(r'[0-9]+(\.[0-9]*)?([Ee][+-]?[0-9]+)?(L|l|LL|ll|F|f|WB|wb|F|f|DF|df|DD|dd|DL|dl)?')
hexnum = re.compile(r'0[Xx][0-9a-fA-F]+(\.[0-9a-fA-F]*)?([Pp][+-]?[0-9a-fA-F]+)')
binnum = re.compile(r'0[Bb][01]+')
wspace = re.compile(r'\s+')
litchr = re.compile(r"'([^'\\\n]|\\.)'")
litstr = re.compile(r'(u8|u|U|L)?"([^"\\\n]|\\.)*"')
headst = re.compile(r'<[^>]>')
multic = re.compile(r'/\*([^\*]|\*[^/])*\*/', flags=re.DOTALL)
singlc = re.compile(r'//.*')

ops = ['->', '++', '--', '<<', '>>', '<=', '>=', '==', '!=', '&&', '||', '::', '...', '*=', '/=', '%=', '+=', '-=', '<<=', '>>=', '&=', '^=', '|=', '##', '<:', ':>', '<%', '%>', '%:', '%:%:']


def csplit(string):
	result = []
	
	i = 0
	
	while i < len(string):
		for pattern in [word, number, hexnum, binnum, wspace, litchr, litstr, headst, multic, singlc]:
			m = pattern.match(string[i:])
			
			if m:
				result.append(m[0])
				i += len(m[0])
				break
		else:
			for op in ops:
				if string[i:i+4].startswith(op):
					result.append(op)
					i += len(op)
					break
			else:
				result.append(string[i])
				i += 1
	
	return result


if __name__ == '__main__':
	from pathlib import Path
	from sys import argv
	
	if len(argv) > 1:
		print(csplit(Path(argv[1]).read_text()))
	else:
		try:
			while True:
				print(csplit(input("Input to csplit: ")))
		except KeyboardInterrupt:
			pass
