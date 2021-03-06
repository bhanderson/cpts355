#!/usr/bin/env python
import sys, re

# A simple postscript interpreter. It provides only minimal error
# checking.
#
# Carl Hauser
# 27 October 2006

# Define a separate function for each arithmetic and boolean 
# primitive function

# Arithmetic ops: each take two numbers and return a number
def plus(x,y):
    return x+y

def minus(x,y):
    return x-y

def times(x,y):
    return x*y

def divide(x,y):
    return x/y

# Comparisons take two numbers and return a boolean
def eq(x,y):
    return x==y

def lt(x,y):
    return x<y

def gt(x,y):
    return x>y

def le(x,y):
    return x<=y

def ge(x,y):
    return x>=y

# Map the postscript operator names to the above functions
# using a dictionary
binops={
    "add": plus,
    "sub": minus,
    "mul": times,
    "div": divide,
    "eq": eq,
    "lt": lt,
    "gt": gt,
    "le": le,
    "ge": ge,
}

# This is the global operand stack
stack = []

# and this the global dictionary stack
dictStack = [{}]

def printStack():
   print('---Top---')
   for elt in reversed(stack):
      print(elt)
   print('---Bottom---')

# We need to recognize postscript names, which start with
# slash and a letter, followed by other characters
name = re.compile('/[a-zA-Z?].*')

# How could defined(t) and definition(t) be handled more
# elegantly? There is currently much code duplication and
# the way they are used we first call defined and then definition
# which means the work is done twice.

# look for name t in the dictionary stack, returning a boolean
# Note the assumption that the warmest end of dictStack is at 
# position 0.
def defined(t):
    # note that dictStack is non-local in this function
    for d in dictStack:
        if t in d: return True
    return False

# look for name t in the dictionary stack, returning either
# its defined value or None if not found
def definition(t):
    for d in dictStack:
        if t in d: return d[t]
    return None

# Having seen a { read input to the
# matching }, returning the code between the braces
# and the position following the }
def readCode(tokens, p):
    code = []
    braceCount = 1
    # it is not clear how best to use a for loop here.
    # invariant: p points at the next tokent to be read
    while True:
        t = tokens[p]
        p += 1
        if t=='}':
            braceCount = braceCount - 1
            if braceCount==0:
                break
        elif t=='{':
            braceCount = braceCount + 1
        code.append(t)
    # invariant tells us this is the correct value of  p to return
    return code, p
    
# The main guts of the interpreter
def evalLoop(tokens):
    # stack and dictStack are declare global because they are updated within
    # evalLoop. If they were not made global then local variables with the
    # same name would be created 
    global stack, dictStack
    p = 0
    # invariant: p points one position past the last
    # token processed, whether that is the token after t
    # or after a code array beginning at t
    while p < len(tokens):
        t = tokens[p]
        p += 1
        
        # handle the binary operators
        if t in binops.keys():
            op = binops[t]
            if len(stack)>1:
                stack[-2:] = [op(stack[-2],stack[-1])]
            else:
                print("not enough operands for", t)

        # handle an opening brace - read to the 
    # matching brace and push the resulting code array
        # on the operand stack
        elif t=='{':
            code, p = readCode(tokens, p)
            stack.append(code)

        # the stack operations exch, pop, clear are easy
        # should add error checking
        elif t=='exch':
            stack[-2:] = [stack[-1],stack[-2]]
        elif t=='pop':
            stack.pop()
        elif t=='clear':
            stack = []
        elif t=='stack':
            printStack()

        # handle def
        elif t=='def':
            if len(stack)>1 and type(stack[-2])==type(''):
                dictStack[0][stack[-2]] = stack[-1]
                stack[-2:] = []
            else: print("invalid operands for", t)

        # handle if
        elif t=='if':
            if len(stack)>1 and type(stack[-1])==type(True) and type(stack[-2])==type([]):
                code = stack.pop()
                cond = stack.pop()
                if cond:
                    # recursively process the true branch code
                    evalLoop(code)
            else: print("invalid operands for" , t)

        # handle ifelse  
        elif t=='ifelse':
        # ifelse is similar but takes two code arrays as args
            if (len(stack)>1 and type(stack[-3])==type(True)
                             and type(stack[-2])==type([])
                             and type(stack[-1])==type([])):
                elsecode = stack.pop()
                ifcode = stack.pop()
                cond = stack.pop()
                if cond:
                    code = ifcode
                else:
                    code = elsecode
                evalLoop(code)
            else: print("invalid operands for" , t)

        # handle dict
        # dict explicitly puts a dictionary on the operand stack
        elif t=='dict':
            stack[-1] = {} # slightly evil: pop and push in one operation
        # begin removes and dictionary from the op stack and puts
        # it on the dict stack

        ### This interpreter keeps the "warm" end of the dict stack
        ### at position 0. This is probably not the best choice for
        ### implementing static links!
        # handle begin/end
        elif t=='begin':
            d = stack.pop()
            if type(d)==type({}):
                dictStack.insert(0,d)
            else:
                print("invalid operands for", t)
        # end removes the top dictionary from the dict stack
        elif t=='end':
            dictStack.pop(0)

        # Use regular expression match to see if the token
        # t is a name constant, e.g. /abc123; if so push it
        elif name.match(t):
            stack.append(t[1:])

        # Is it a name defined in a postscript dictionary?
        elif defined(t):
            defn = definition(t)
            # if the definition is a code array it needs to be
            # called so push the current context on the execution
            # stack (by recursively calling evalLoop) and start executing it
            if type(defn)==type([]):
                evalLoop(defn)
            else:
            # otherwise, just push the value on the op stack
                stack.append(defn)
        else:
    # if nothing else works try to interpret it as a number
            try:
                 # if it is a number push it
                 stack.append(float(t))
            except:
             # otherwise, it's an error
                 print(t,  " is not a valid token")
    return


evalLoop( re.findall( '/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]',
                      ' '.join(open(sys.argv[1]).readlines())
                      )
          )

printStack()
