#!/usr/bin/python3
import re
import sys

pattern = '/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]|%.*|[^\t\n ]'
names = re.compile('/[a-zA-Z0-9?].*')
# /? has a slash in front
# * 0 or more
# token can be right or left brace
# token can be percent sign
# .* can be any character
# ^ any character that is not a tab or newline
# A simple program
opstack = []
dicstack = [{}]
gstack = []
exstack = []


brackets = {
        "{": 1,
        "}": -1,
        "[": 1,
        "]": -1,
        "(": 1,
        ")": -1,
        "<": 1,
        ">": -1,
        }

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

def defined(d):
	for x in dictStack:
		if d in x.keys():
			return x[d]
		else:
			return None


def pfindmatch(tokens, pos):
    tempstack = []
    count = 1
    while pos < len(tokens) and count > 0:
        a = tokens[pos]
        pos +=1
        if a in brackets.keys():
            count += brackets[a]
        else:
            tempstack.append(a)
    return tempstack, pos

def printStacks():
    print("***opstack***")
    for x in reversed(opstack):
        print(x)
    print("***dicstack***")
    for x in reversed(dicstack):
        print(x)
    print("***gstack***")
    for x in reversed(gstack):
        print(x)
    print("***exstack***")
    for x in reversed(exstack):
        print(x)

def error(s):
    print("you received a(n) %s error. Whooops\n" % s)
    print("opstack: %s\n" % opstack)
    print("dicstack: %s\n" % dicstack)
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
    #tokens = parse("3 2 add 2 add 10 add (string one)(take two) false stack")
    tokens = parse("1 2 3 {/x 4 def} stack")
    print(tokens)
    pos = 0
    while pos < len(tokens):
        tok = tokens[pos]
        pos += 1
        try:
            opstack.append(float(tok))
        except:
            if tok in ops.keys() and len(opstack)>1:
                op = ops[tok]
                opstack[-3:] = [op(opstack[-2],opstack[-1])]
            elif tok in brackets.keys():
                code, pos = pfindmatch(tokens, pos)
                opstack.append(code)
            # stack operands
            elif tok == 'true':
                opstack.append(True)
            elif tok == 'false':
                opstack.append(False)
            elif tok == 'pop':
                opstack.pop()
            elif tok == 'clear':
                opstack = []
            elif tok == 'stack':
                printStacks()
            elif tok == '=':
                print(opstack.pop())
            elif tok == fun.match(tok):
                opstack.append(token[1:])
            elif tok == 'def':
                if len(opstack)>1 and type(opstack[-2])==str:
                    tempD = {opstack[-2]:opstack[-1]}
                    opstack[-2:] = []
            else:
                error(tok)
