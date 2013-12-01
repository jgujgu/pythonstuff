import sys

def q1(daFile):

    blank = []
    for x in open(daFile):
        blank.append(x.strip())
    return(blank)


def q2(daFile):
    empty = []
    for x in open(daFile):
        empty.append(x.strip().split('$$$'))
    return (empty)

def q3(daFile):
    none = q2(daFile)
    myDictionary = {}
    for x in none:
        myDictionary[x[0]] = x[1]
    return myDictionary


def q4(daFile):
    if sys.version_info[0] > 2:
        f = open('test.txt', 'r', encoding="utf8")
    elif sys.version_info[0] == 2:
        f = open('test.txt', 'r')
    some = [x.strip() for x in f]
    Dict = {}
    for y in some:
        Dict[y] = Dict.get(y,0)+1
    Out = []
    for x in sorted(Dict):
        if len(x)>2:
            Out+= [x+ " occurs " + str(Dict[x]) + " times."]
    return Out
    
