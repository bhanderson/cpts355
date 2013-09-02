from collections import Counter
def testttrans():
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

def testhisto():
    if histo("tests") != histo("sstte"): return False
    return True

def histo(s):
    cnt = Counter(s)
    d = dict(cnt)
    return sorted(d.items(), key=lambda item: -item[1])

def testdigraphs():
    t =  digraphs("hello worldll")
    if t[0][1] != 1: return False
    return True

def digraphs(s):
    n = list(s)
    i = 0
    while i < len(n)-1:
        k = '/'+n[i]+n[i+1]+'/'
        if k not in [x[0] for x in n]:
            n[i] = ('/' + n[i] + n[i+1]+ '/', 0)
            i+=1
        else:
            pos = [x[0] for x in n].index(k)
            n[pos] = (n[pos][0], n[pos][1]+1)
            n.pop(i)
    n.pop()
    n = sorted(n, key=lambda tup: tup[1], reverse=True)
    return n
if __name__ == "__main__":
    from hw1 import *
    passedMsg = "%s passed"
    failedMsg = "%s failed"
    if testttrans():
        print ( passedMsg % 'testtrans' )
    else:
        print ( failedMsg % 'testtrans' )
    if testhisto():
        print ( passedMsg % 'testhisto' )
    else:
        print ( failedMsg % 'testhisto' )
    if testdigraphs():
        print ( passedMsg % 'testdigraphs' )
    else:
        print ( failedMsg % 'testdigraphs' )
