import numpy as np
import src.alg.dpll_unit as udpll
import os

# generate cnf with desired properties

# clauseNumDet 
# tells us weather we want a fixed number of clauses ("DET") or want some variablility "ND", then the
# value we gave is the mean and values are normal distriubted around it

# clauseLenDet
# analogous

def generateCNF(varNum,clauseNum,clauseNumDet,clauseLen,clauseLenDet):
    
    # initiate list of clauses
    clauseList = list()
    
    # generate list of literals
    varList = np.linspace(1,varNum,varNum).astype(int)
    varList = np.concatenate((varList,-varList))
    
    if clauseNumDet == "DET":
        numClaus = clauseNum
    elif clauseLenDet == "ND":
        numClaus = np.random.normal(clauseNum, clauseNum/2, 1).astype(int)   
    #print("numClaus",numClaus)
    
    while len(clauseList) < numClaus:
        newClause = np.array([])
    
        if clauseLenDet == "DET":
            lenClause = clauseLen
        elif clauseLenDet == "ND":
            lenClause = np.random.normal(clauseLen, clauseLen/2, 1).astype(int)
            if lenClause < 2:
                lenClause = 2
            elif lenClause > varNum:
                lenClause = varNum
            else:
                pass
            
        #print("lenClause",lenClause)

        while len(newClause) < lenClause:
            #print(newClause)
            newVar = np.random.choice(np.setdiff1d(varList,np.concatenate([newClause, -newClause])))
            if not newVar in newClause and not -newVar in newClause:
                newClause = np.append(newClause,newVar)

        #newClause = np.append(newClause,0)

        # if first entry contains only zeros (as set in the beginning) overwrite with new clause
        #if not clauseList[0].any():
        #    clauseList[0] = newClause
        #else:
        #    clauseList = np.concatenate((clauseList,[newClause])).astype(int)
        clauseList.append(newClause)
        
    #print("ddpll says",udpll.output(list(clauseList),heuristics="DLIS")[0])
    SAT = udpll.output(clauseList,heuristics="DLIS")[0]
        
    return(SAT,clauseList)

def output(path,n=200,varNum=20,clauseNum=100,clauseNumDet="DET",clauseLen=3,clauseLenDet="DET"):

    name = "".join([str(varNum),"vars_",clauseNumDet,str(clauseNum),"clauseCount_",clauseLenDet,str(clauseLen),"clauseLength"])
    
    out_path_SAT = "".join([path,name,"_SAT"])
    out_path_unSAT = "".join([path,name,"_unSAT"])
    os.mkdir(out_path_SAT)
    os.mkdir(out_path_unSAT)

    SATcount = 0
    unSATcount = 0
    attemts = 0

    #tree_dat = open(out_path,"w+")

    while ((SATcount < n) or (unSATcount < n)) and attemts <= n*20:
        (SAT,clauseList) = generateCNF(varNum,clauseNum,clauseNumDet,clauseLen,clauseLenDet)
        attemts = attemts + 1
        #print(SAT)

        if (SAT==True) and (SATcount < n):
            SATcount = SATcount+1
            out_path = "".join([out_path_SAT, "/SAT_",str(SATcount),".cnf"])
            cnfFile = open(out_path,"w+")

            cnfFile.write("".join(["c","\n"]))
            cnfFile.write("".join(["c              vars   ",str(varNum),"\n"]))
            cnfFile.write("".join(["c     clause Number   ",clauseNumDet,"(",str(clauseNum),")","\n"]))
            cnfFile.write("".join(["c     clause length   ",clauseLenDet,"(",str(clauseLen),")","\n"]))
            cnfFile.write("".join(["c              SAT?   ",str(SAT),"\n"]))
            cnfFile.write("".join(["c","\n"]))
            cnfFile.write("".join(["p cnf ",str(varNum)," ", str(clauseNum),"\n"]))
            for line in clauseList:
                cnfFile.write("".join(["".join("".join([str(x.astype(int))," "]) for x in line),"0","\n"]))
            cnfFile.write("% \n")
            cnfFile.write("0 \n")
            cnfFile.close
        
        elif (SAT==False) and (unSATcount < n):
            unSATcount = unSATcount+1
            out_path = "".join([out_path_unSAT, "/unSAT_",str(unSATcount),".cnf"])
            cnfFile = open(out_path,"w+")

            cnfFile.write("".join(["c","\n"]))
            cnfFile.write("".join(["c              vars   ",str(varNum),"\n"]))
            cnfFile.write("".join(["c     clause Number   ",clauseNumDet,"(",str(clauseNum),")","\n"]))
            cnfFile.write("".join(["c     clause length   ",clauseLenDet,"(",str(clauseLen),")","\n"]))
            cnfFile.write("".join(["c              SAT?   ",str(SAT),"\n"]))
            cnfFile.write("".join(["p cnf ",str(varNum)," ", str(clauseNum),"\n"]))
            for line in clauseList:
                cnfFile.write("".join(["".join("".join([str(x.astype(int))," "]) for x in line),"0","\n"]))
            cnfFile.write("% \n")
            cnfFile.write("0 \n")
            cnfFile.close
    
    print("".join([name,": Wrote a total of ",str(SATcount)," satisfiable CNFs and ",str(unSATcount)," not satisfiable ones"]))

def runTests(path):
    #output(path,50,20,300,"ND",3,"ND")
    #output(path,50,60,300,"ND",3,"ND")

    # run heuristic tests for the presentation on 
    output(path,50,20,100,"DET",3,"DET")
    output(path,50,20,100,"DET",5,"DET")
    output(path,50,20,300,"DET",3,"DET")
    output(path,50,20,300,"DET",5,"DET")
    output(path,50,60,100,"DET",3,"DET")
    output(path,50,60,100,"DET",5,"DET")
    output(path,50,60,300,"DET",3,"DET")
    output(path,50,60,300,"DET",5,"DET")
    output(path,50,100,100,"DET",3,"DET")
    output(path,50,100,100,"DET",5,"DET")
    output(path,50,100,300,"DET",3,"DET")
    output(path,50,100,300,"DET",5,"DET")

    #generate trees for graph making
    #output(path,10,6,20,"DET",3,"DET")
