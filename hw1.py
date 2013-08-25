# function to test translation code
# return True if successful, False if any test fails
def testtrans():
    ttable = makettable('abc', 'xyz')
    revttable = makettable('xyz', 'abc')
    tests = "Now I know my abc's"
    answer = "Now I know my xyz's"
    if trans(ttable, tests) != answer: return False
    if trans(revttable, trans(ttable, tests)) != "Now I know mb abc's": return False
    if trans(ttable,'') != '': return False
    if trans(makettable('',''), "abc") != 'abc': return False
    return True

def trans(ttable, s):
	l = list(s)
	for i,item in enumerate(l):
		l[i] = ttable.get(item, item)
	return ''.join(l)

def makettable(s1, s2):
	d = {}
	for i,item in enumerate(s1):
		d[item] = s2[i]
	return d
