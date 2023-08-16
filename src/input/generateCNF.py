import numpy as np
import src.alg.dpll as dpll
import os
import csv

# generate a single cnf with desired properties
def generateCNF(varNum,clauseNum,clauseNumDet,clauseLen,clauseLenDet):

    # clauseNumDet 
    # tells us weather we want a fixed number of clauses ("DET") or want some variablility "ND", then the
    # value we gave is the mean and values are normal distriubted around it

    # clauseLenDet
    # analogous
    
    # initiate list of clauses
    clauseList = list()
    
    # generate list of literals
    varList = np.linspace(1,varNum,varNum).astype(int)
    varList = np.concatenate((varList,-varList))
    
    # set length of clauses
    if clauseNumDet == "DET":
        numClaus = clauseNum
    elif clauseNumDet == "ND":
        numClaus = np.random.normal(clauseNum, clauseNum/2, 1).astype(int)   
    
    # generate the clauses
    while len(clauseList) < numClaus:
        newClause = np.array([])
    
        # set clause length for currently generated clause
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

        # fill up clause with literals it does not already contain
        while len(newClause) < lenClause:
            newVar = np.random.choice(np.setdiff1d(varList,np.concatenate([newClause, -newClause])))
            if not newVar in newClause and not -newVar in newClause:
                newClause = np.append(newClause,newVar)
        clauseList.append(newClause)
        
    # test satisfiability
    SAT = dpll.output_udpll(clauseList,heuristics="DLIS")[0]
        
    return(SAT,clauseList)

# generate two folders containing a specified number of satisfiable and not satisfiable cnfs with given properties
def output(path,n=200,varNum=20,clauseNum=100,clauseNumDet="DET",clauseLen=3,clauseLenDet="DET"):

    # generate a name for the foder in which the cnfs will be safed
    name = "".join([str(varNum),"vars_",clauseNumDet,str(clauseNum),"clauseCount_",clauseLenDet,str(clauseLen),"clauseLength"])
    
    # generate the folders to generate the satisfiable and the not satisfiable files under
    out_path_SAT = "".join([path,name,"_SAT"])
    out_path_unSAT = "".join([path,name,"_unSAT"])
    os.mkdir(out_path_SAT)
    os.mkdir(out_path_unSAT)

    # set counters to keep track of generated formulas throughout the function
    SATcount = 0
    unSATcount = 0
    attemts = 0

    # continue generating formulas unit either the desired amount was generated or we tried generating 10 times the amount of 
    # formulas we wanted to generate. This is necessary to prevent the programm running endlessly if parameter combinations were
    # specified that would likeely not lead to satisfiable or unsatisfiable cnfs.
    while ((SATcount < n) or (unSATcount < n)) and attemts <= n*10:

        # generate a cnf
        (SAT,clauseList) = generateCNF(varNum,clauseNum,clauseNumDet,clauseLen,clauseLenDet)
        attemts = attemts + 1

        # and test if it was SAT or unSAT and weather the desired amount of files in the cathegory wasnt reached already. 
        # Then write the headers for the file and the cnf itself to a newly generated file in the generated folder

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
        
        # same for not satisfiable cnf

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


def multipleCNFs(path):

    # specify the name of the folder to save the files under
    dirname = "benchmarkCNFs"

    # generate a name for the folder that is not already taken
    i = 1
    while dirname in os.listdir(os.path.dirname(path)):
        dirname = "".join([dirname,str(i)])
        i = i+1

    # create the folder
    dirPath="".join([os.path.dirname(path),"/",dirname,"/"])
    os.mkdir(dirPath)

    # extract information form the csv file containing the config
    with open(path, newline='') as csvfile:
        config = csv.DictReader(csvfile)
        for row in config:
            number = int(row["Number"])
            varCount = int(row["Vars"])
            ClauseCount = int(row["ClauseCount"])
            ClauseCountDet = row["ClauseCountDet"]
            ClauseLength = int(row["ClauseLen"])
            ClauseLengthDet = row["ClauseLenDet"]
            # create cnfs with properties in generated folder
            output(dirPath,number,varCount,ClauseCount,ClauseCountDet,ClauseLength,ClauseLengthDet)
            print("".join(["generated files ",str(varCount),"vars_",ClauseCountDet,str(ClauseCount),"clauseCount_",ClauseLengthDet,str(ClauseLength),"clauseLength"]))
