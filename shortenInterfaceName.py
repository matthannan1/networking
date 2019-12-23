import re


def shortenInt(port):
    re1 = '(.)'        # Any Single Character 1
    re2 = '(.)'	       # Any Single Character 2
    re3 = '.*?'	       # Non-greedy match on filler
    re4 = '(\\d+)'     # Integer Number 1
    re5 = '(\\/)'	   # Any Single Character 3
    re6 = '(\\d+)'	   # Integer Number 2

    rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6, re.IGNORECASE | re.DOTALL)
    m = rg.search(port)
    if m:
        c1 = m.group(1)
        c2 = m.group(2)
        int1 = m.group(3)
        c3 = m.group(4)
        int2 = m.group(5)
        # print("("+c1+")"+"("+c2+")"+"("+int1+")"+"("+c3+")"+"("+int2+")"+"\n")
        shortInt = c1+c2+int1+c3+int2
        return shortInt
