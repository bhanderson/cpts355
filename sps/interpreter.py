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
opstack = []
distack = [{}]
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

def padd(a, b):
	return float(a) + float(b)
def psub(a, b):
	return float(a) - float(b)
def pmul(a, b):
	return float(a) * float(b)
def pdiv(a, b):
	return float(a) / float(b)
def peq(a, b):
	return float(a) == float(b)
def plt(a, b):
	return float(a) < float(b)
def pgt(a, b):
	return float(a) > float(b)
def ple(a, b):
	return float(a) <= float(b)
def pge(a, b):
	return float(a) >= float(b)
def pand(a, b):
	if type(a) and type(b) is bool:
		return a and b
	else:
		return error()
def por(a, b):
	if type(a) and type(b) is bool:
		opstack.append(a or b)
	else:
		return error()
def pnot(a):
	if type(a) is bool:
		opstack.append(not a)
	else:
		return error()
def dup(a):
	a.append(a[-1])
def exch(a):
	a[-1], a[-2] = a[-2], a[-1]
def pop(a):
	a.pop()
def dictz():
	return dict()
def stack(s):
	print(s)
def ptop(a):
	print(a.pop())
def error():
	print("you received an error. Whooops\n")

ops = {
		"add": padd,
		"sub": psub,
		"mul": pmul,
		"div": pdiv,
		"eq": peq,
		"lt": plt,
		"gt": pgt,
		"le": ple,
		"ge": pge,
		"and": pand,
		"or": por,
		"not": pnot,
		}
# command line use: pass the filename as the first command-line argument
if __name__ == "__main__":
	#fn = sys.argv[1]
	#print (parseFile(open(fn, 'r')))
	print (parse(demoProg))
	tokens = parse(demoProg)
