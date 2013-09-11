#!/usr/bin/python3
import re
import sys

pattern = '/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]|%.*|[^\t\n ]'
# /? has a slash in front
# * 0 or more
# token can be right or left brace
# token can be percent sign
# .* can be any character
# ^ any character that is not a tab or newline
# A simple program
demoProg = '''
/fact {
	1 dict begin
	/x exch def
		x 0 eq
		{1}
		{x 1 sub fact x mul}
	ifelse
	end
} def
'''
def parse(s):
	"""Given a string, return the tokens it contains"""
	tokens = re.findall(pattern ,s)
	return tokens

def parseFile(f):
	"""Given an open file, return the tokens it contains"""
	tokens = parse(''.join(f.readlines()))
	return tokens

# command line use: pass the filename as the first command-line argument
if __name__ == "__main__":
	fn = sys.argv[1]
	print (parseFile(open(fn, 'r')))
