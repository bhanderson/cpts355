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
dicstack = [{}]
count = 0

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
    dictz begin
    /x exch def
        x 0 eq
        {1}
        {x 1 sub fact x mul}
    ifelse
    end
} def
9 fact '''

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
def exch():
    if len(opstack)>1:
        opstack[-2], opstack[-1] = opstack[-1], opstack[-2]
        return
    sys.exit()
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
    while True:
        a = tokens[pos]
        pos = pos + 1
        if a == '}':
            count = count -1
            if count == 0:
                break
        elif a =='{':
            count = count + 1
        tempstack.append(a)
    return tempstack, pos

def printStacks():
    print("***opstack***")
    for x in reversed(opstack):
        print(x)
    print("***dicstack***")
    for x in reversed(dicstack):
        print(x)

def error(s):
    print("you received a(n) %s error. Whooops\n" % s)
    print("opstack: %s\n" % opstack)
    print("dicstack: %s\n" % dicstack)
    sys.exit()

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

def pseval(tokens):
    global opstack
    global dicstack
    tempstack = []
    pos = 0
    while pos < len(tokens):
        tok = tokens[pos]
        pos += 1
        try:
            opstack.append(float(tok))
        except:
            if tok in ops.keys() and len(opstack)>1:
                op = ops[tok]
                opstack[-2:] = [op(opstack[-2],opstack[-1])]
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
            elif tok == 'exch':
                exch()
            elif tok == 'clear':
                opstack = []
            elif tok == 'stack':
                printStacks()
            elif tok == '=':
                print(opstack.pop())
            elif tok[0] == '/':
                opstack.append(tok[1:])
            elif tok == 'if':
                a = opstack.pop()
                b = opstack.pop()
                if b == True and type(a) == list:
                    pseval(a)
            elif tok == 'ifelse':
                a = opstack.pop()
                b = opstack.pop()
                c = opstack.pop()
                if type(a) == list and type(b) == list and c == True:
                    pseval(b)
                else:
                    pseval(a)
            elif tok == 'def':
                dicstack[-1][opstack.pop()] = opstack.pop()
            elif tok == 'begin':
                if type(tempstack) == dict:
                    dicstack.append(tempstack)
            elif tok == 'end':
                dicstack.pop()
            elif tok == 'dictz':
                tempstack = dictz()
            elif type(tok) == list:
                print("token: %s" % tok)
                pseval(tok)
            else: # variable name
                found = False
                for x in dicstack:
                    if tok in x.keys():
                        found = True
                        if type(x[tok]) == list:
                            pseval(x[tok])
                            continue
                        opstack.append(x[tok])
                        continue
                if not found:
                    error(tok)

# command line use: pass the filename as the first command-line argument
if __name__ == "__main__":
    #fn = sys.argv[1]
    #print (parseFile(open(fn, 'r')))
    #tokens = parse("3 2 add 2 add 10 add (string one)(take two) false stack")
    #tokens = parse("/x 4 def /f { 1 3 add } def x f add =")
    #tokens = parse("3 4 add /x {3 2 add} def x add =")
    #tokens = parse("3 dict stack")
    #tokens = parse("0 1 eq {3} if stack")
    #tokens = parse("1 0 eq {3} {4} ifelse =")
    #tokens = parse(" 7 3 4 add stack")
    #tokens = parse("3 2 add stack")
    #tokens = parse("1 dictz /x 4 def begin /y 5 def ")
    #tokens = parse("/x 3 def")
    #tokens = parse("9 /x exch def")
    #tokens = parse(" 3 4 3 4 exch")
    #tokens = parse(demoProg)
    #tokens = parse("1 0 eq")
    #tokens = parse(" 1 2 3 4 sub")
    #tokens = parse("9 dictz begin /x exch def x 0 eq")
    #tokens = parse("{1{2{3}}}")
    pseval(tokens)
    print("      opstack     ")
    print("==================")
    for x in opstack:
        print(x)
        print("------------------")
    print("==================")
    print("      dicstack    ")
    print("==================")
    for x in dicstack:
        print(x)
        print("------------------")
    print("==================")

