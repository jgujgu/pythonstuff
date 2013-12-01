import re
import sqlite3

re.findall(r'\S{0,}','4,382     Inventories:     Leaf tobacco')

def kwicn(daTerm, docStr, n):


    return re.findall((r'\w{0,}\W+'*n)+daTerm+(r'\W+\w{0,}'*n)+r'\W',re.sub(r'\n+|\\n+',' ',docStr),re.IGNORECASE)
    

def dbkwicn(daCurs,docID,daTerm, n):

    sql = '''select doc from docs where id = '''+str(docID)

    
    for docStr in daCurs.execute(sql):
       
        out=kwicn(daTerm, str(docStr), n)
   
	
        
    return out

    
def listOfFirms(daCurs):

    sql = '''select distinct firm from docs'''
    out=[]
    for docStr in daCurs.execute(sql):

        out.append(docStr[0])


    return out

def listOfRTypes(daCurs):

    sql = '''select distinct reporttype from docs'''
    out=[]
    for docStr in daCurs.execute(sql):

        out.append(docStr[0])


    return out


def listOfYears(daCurs):

    sql = '''select distinct year from docs'''
    out=[]
    for docStr in daCurs.execute(sql):

        out.append(docStr[0])


    return out

def getConceptList(conceptName):

    con = sqlite3.connect('ConceptVocabularies.sqlite')
    cur = con.cursor()
    sql = '''select * from concept'''
    out=[]
    for docStr in cur.execute(sql):

        if docStr[0]==conceptName:
            out.append(docStr[1])

    con.close()
    out.sort(key=lambda x: x.lower())
    return out

def scoreDocConceptCountScore(doc, conceptName):

    ConceptList=getConceptList(conceptName)
    out=0
    for Concept in ConceptList:
        out=out+len(re.findall(Concept,doc,re.IGNORECASE))

    return out

def scoreDocGroup(firm,year,rtype,cName,daCurs):

    sql = '''select * from docs'''
    out=0
    for docStr in daCurs.execute(sql):
        if docStr[1]==firm and docStr[2]==year and docStr[4]==rtype:
            out=out+scoreDocConceptCountScore(docStr[5], cName)

    return out

def timeScores(firm,years,rtype,cName,daCurs):

    out=[]
    for year in years:
        out.append(scoreDocGroup(firm,year,rtype,cName,daCurs))
    return out

def timeScoresIndustryReport(cName, daCurs):

    FileName='''output.txt'''
    years=listOfYears(daCurs)
    firms=listOfFirms(daCurs)
    rtypes=listOfRTypes(daCurs)
    f = open(FileName, 'w')
    newLine='''Concept name:,'''+cName+'''\n'''

    f.write(newLine)
    
    newLine='''For years:,'''
    for year in years:
        newLine=newLine+''','''+str(year)
    newLine=newLine+'''\n'''

    f.write(newLine) 
    newLine='''Firms,Report types\n'''

    f.write(newLine)
    
    for firm in firms:
        for rtype in rtypes:
            scoreOutputs=timeScores(firm,years,rtype,cName,daCurs)
            newLine=firm+''','''+rtype
            for scoreOutput in scoreOutputs:
                newLine=newLine+''','''+str(scoreOutput)
            newLine=newLine+'''\n'''

            f.write(newLine)
            
    f.close()       

    return ''
