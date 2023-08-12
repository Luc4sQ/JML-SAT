# Importing some stuff
import numpy as np
import os
import src.input.dimacs as sid
import src.alg.bruteforce as br
import src.timing.measure as ms
import src.alg.dpll as dpll
import src.alg.dpll_unit as udpll
import src.alg.dpll_unit_ple as udpllple
import src.alg.dpll_ple as dpllple
import src.alg.dp as dp
import src.alg.dpll_visual as dpll_visual
import src.alg.dpll_unit_visual as udpll_visual

#######################################################################################################
########### DPLL, uDPLL AND uDPLLple ##################################################################
#######################################################################################################

def dpllComp(path):

    selfGeneratedCNF = True

    # TODO: if no CNFs are in folder, print error
    if not path.endswith("/"):
        print("ERROR: path for a folder with CNFs needs to be provided")
        
    else:

        out_path = "".join([path, "SATstats.txt"])
        stats_dat = open(out_path,"w+")

        # TODO: add info about System test was run on, date and time, ...

        files = os.listdir(path)

        # create control points at which a status update will be printed in the terminal (if more than 20 formulas are in folder)
        stepCount = 50
        controlPoints = np.array([])
        if len(files) >= stepCount:
            for j in range(1,stepCount):
                controlPoints = np.append(controlPoints,files[j*round(len(files)/stepCount)])
        
        #print(controlPoints)
            

        # define the empty arrays in which the stats will be written during the actual measurements
        DPLLresList = np.array([])
        uDPLLresList = np.array([])
        DPLLpleresList = np.array([])
        uDPLLpleresList = np.array([])

        SATcount = 0
        CNFcount = 0

        # iterativeley measure time it took to determine satisfiablilty for each of the algorythms
        for file in files:
            print(file,path)
            #TODO: sinnvolle Fehlermeldung hinzufügen
            #print(file)
            if file.endswith("cnf"):

                CNFcount = CNFcount + 1

                wholePath = "".join([path,file])
                cnf, properties = sid.FileReader(wholePath)

                print("DPLL")
                timeDPLL, (satisfiableDPLL, variableAssignment) = ms.timeInSeconds(dpll.output, cnf)

                print("dDPLL")
                timeUDPLL, (satisfiableUDPLL, variableAssignment) = ms.timeInSeconds(udpll.output, cnf)

                print("DPLLple")
                timeDPLLple, (satisfiableDPLLple, variableAssignment) = ms.timeInSeconds(dpllple.output, cnf)

                print("uDPLLple")
                timeUDPLLple, (satisfiableUDPLLple, variableAssignment) = ms.timeInSeconds(udpllple.output, cnf)

                if not satisfiableDPLL == satisfiableUDPLL and satisfiableDPLL == satisfiableUDPLLple and satisfiableDPLL == satisfiableDPLLple:
                    print("ERROR: file",file,"resulted in different SAT results: DPLL:",satisfiableDPLL,"uDPLL:",satisfiableUDPLL,"uDPLLple:",satisfiableUDPLLple)
                else:
                    SATcount = SATcount+1
                    DPLLresList = np.append(DPLLresList,timeDPLL)
                    uDPLLresList = np.append(uDPLLresList,timeUDPLL)
                    DPLLpleresList = np.append(DPLLpleresList,timeDPLLple)
                    uDPLLpleresList = np.append(uDPLLpleresList,timeUDPLLple)

            if file in controlPoints:
                print("".join((str((np.where(controlPoints==file)[0][0]+1)*(100/stepCount)),"% of files processed \n")))

        #set parameter determining how many decimales to round to in result
        decimals = 4

        # calculate mean and std and write to file
        stats_dat.write("Comparison of DPLL, DPLL with Unit Resolution (uDPLL) and of DPLL with Unit Resolution and Pure Literal Elimination (uDPLLple) \n\n")
        stats_dat.write("".join(["Tests were run on ",str(len(files))," CNF formulas \n\n"]))
        stats_dat.write("\n\nSummary: \n\n")
        stats_dat.write("Average time to determine satifyability in seconds: \n")
        stats_dat.write("".join(["DPLL: ",str(round(np.mean(DPLLresList),decimals)),"  uDPLL: ",str(round(np.mean(uDPLLresList),decimals)),"  DPLLple: ",str(round(np.mean(DPLLpleresList),decimals)),"  uDPLLple: ",str(round(np.mean(uDPLLpleresList),decimals)),"\n\n"]))
        stats_dat.write("Standard deviation of time to determine satifyability in seconds: \n")
        stats_dat.write("".join(["DPLL: ",str(round(np.std(DPLLresList),decimals)),"  uDPLL: ",str(round(np.std(uDPLLresList),decimals)),"  DPLLple: ",str(round(np.std(DPLLpleresList),decimals)),"  uDPLLple: ",str(round(np.std(uDPLLpleresList),decimals)),"\n\n"]))
        stats_dat.write("".join(["Overall ",str(SATcount/CNFcount),"% of CNFs were satisfiable"]))
        stats_dat.close()
        
        # extract meta information from folder name
        # this will only work if folder with CNFs was created by this programm

        if selfGeneratedCNF == True:

            folderName = path.split("/")[-2]
            #print(folderName)
            varNum = folderName.split("vars")[0]
            #print(varNum)
            clausCountDet = "DET" if "vars_DET" in folderName else "ND"
            #print(ClausCountDet)
            clauseCount = folderName.split("clauseCount")[0].split(clausCountDet)[-1]
            #print(ClauseCount)
            clausLenDet = "DET" if "clauseCount_DET" in folderName else "ND"
            #print(ClausLenDet)
            clauseLen = folderName.split("clauseLength")[0].split(clausLenDet)[-1]
            #print(ClauseCount)
            SATstatus = folderName.split("_")[-1]
            #print(SATstatus)

            csv = "".join([SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","DPLL,",str(round(np.mean(DPLLresList),decimals)),",",str(round(np.std(DPLLresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","uDPLL,",str(round(np.mean(uDPLLresList),decimals)),",",str(round(np.std(uDPLLresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","DPLLple,",str(round(np.mean(DPLLpleresList),decimals)),",",str(round(np.std(DPLLpleresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","uDPLLple,",str(round(np.mean(uDPLLpleresList),decimals)),",",str(round(np.std(uDPLLpleresList),decimals)),"\n"])
            
        else:
            csv = ""
        #TODO: print results for all cnfs?

        #print("done")
        return(csv)


def heuristicsComp(path):

    # set a parameter telling us weather the CNF is generated by this program, in this case, information can be extracted from the folder name to create
    # a cnv file containing the results
    # TODO: recognize automatically using regular expressions
    selfGeneratedCNF = True

    # TODO: if no CNFs are in folder, print error
    if not path.endswith("/"):
        print("ERROR: path for a folder with CNFs needs to be provided")
        
    else:
        out_path = "".join([path, "SATstats_heuristics.txt"])
        stats_dat = open(out_path,"w+")

        # TODO: add info about System test was run on, date and time, ...

        files = os.listdir(path)

        # create control points at which a status update will be printed in the terminal (if more than 20 formulas are in folder)
        stepCount = 50
        controlPoints = np.array([])
        if len(files) >= stepCount:
            for j in range(1,stepCount):
                controlPoints = np.append(controlPoints,files[j*round(len(files)/stepCount)])
        
        #print(controlPoints)
            

        # define the empty arrays in which the stats will be written during the actual measurements
        RANDresList = np.array([])
        MOMSresList = np.array([])
        JWOSresList = np.array([])
        JWTSresList = np.array([])
        DLCSresList = np.array([])
        DLISresList = np.array([])

        SATcount = 0
        CNFcount = 0

        # iterativeley measure time it took to determine satisfiablilty for each of the algorythms
        for file in files:
            #TODO: sinnvolle Fehlermeldung hinzufügen
            #print(file)
            if file.endswith("cnf"):

                CNFcount = CNFcount + 1

                wholePath = "".join([path,file])
                
                cnf, properties = sid.FileReader(wholePath)

                timeRAND, (satisfiableRAND, variableAssignment) = ms.timeInSecondsHeuristics(udpll.output, cnf, "RAND")
                timeMOMS, (satisfiableMOMS, variableAssignment) = ms.timeInSecondsHeuristics(udpll.output, cnf, "MOMS")
                timeJWOS, (satisfiableJWOS, variableAssignment) = ms.timeInSecondsHeuristics(udpll.output, cnf, "JWOS")
                timeJWTS, (satisfiableJWTS, variableAssignment) = ms.timeInSecondsHeuristics(udpll.output, cnf, "JWTS")
                timeDLCS, (satisfiableDLCS, variableAssignment) = ms.timeInSecondsHeuristics(udpll.output, cnf, "DLCS")
                timeDLIS, (satisfiableDLIS, variableAssignment) = ms.timeInSecondsHeuristics(udpll.output, cnf, "DLIS")

                if not satisfiableRAND == satisfiableMOMS == satisfiableJWOS == satisfiableJWTS == satisfiableDLCS == satisfiableDLIS:
                    pass
                    print("ERROR: file",file,"resulted in different SAT results!")
                else:
                    SATcount = SATcount+1
                    RANDresList = np.append(RANDresList,timeRAND)
                    MOMSresList = np.append(MOMSresList,timeMOMS)
                    JWOSresList = np.append(JWOSresList,timeJWOS)
                    JWTSresList = np.append(JWTSresList,timeJWTS)
                    DLCSresList = np.append(DLCSresList,timeDLCS)
                    DLISresList = np.append(DLISresList,timeDLIS)

            if file in controlPoints:
                print("".join((str((np.where(controlPoints==file)[0][0]+1)*(100/stepCount)),"% of files processed \n")))

        #set parameter determining how many decimales to round to in result
        decimals = 4

        # calculate mean and std and write to file
        stats_dat.write("Comparison of uDPLL with different search heuristics \n\n")
        stats_dat.write("".join(["Tests were run on ",str(len(files))," CNF formulas \n\n"]))
        stats_dat.write("\n\nSummary: \n\n")
        stats_dat.write("Average time to determine satifyability status in seconds: \n")
        stats_dat.write("".join(["RAND: ",str(round(np.mean(RANDresList),decimals)),"  MOMS: ",str(round(np.mean(MOMSresList),decimals)),"  JWOS: ",str(round(np.mean(JWOSresList),decimals)),"  JWTS: ",str(round(np.mean(JWTSresList),decimals)),"  DLCS: ",str(round(np.mean(DLCSresList),decimals)),"  DLIS: ",str(round(np.mean(DLISresList),decimals)),"\n\n"]))
        stats_dat.write("Standard deviation of time to determine satifyability in seconds: \n")
        stats_dat.write("".join(["RAND: ",str(round(np.std(RANDresList),decimals)),"  MOMS: ",str(round(np.std(MOMSresList),decimals)),"  JWOS: ",str(round(np.std(JWOSresList),decimals)),"  JWTS: ",str(round(np.std(JWTSresList),decimals)),"  DLCS: ",str(round(np.std(DLCSresList),decimals)),"  DLIS: ",str(round(np.std(DLISresList),decimals)),"\n\n"]))
        stats_dat.write("".join(["Overall ",str((SATcount/CNFcount)*100),"% of CNFs were satisfiable"]))
        stats_dat.close()

        
        # extract meta information from folder name
        # this will only work if folder with CNFs was created by this programm

        if selfGeneratedCNF == True:

            folderName = path.split("/")[-2]
            #print(folderName)
            varNum = folderName.split("vars")[0]
            #print(varNum)
            clausCountDet = "DET" if "vars_DET" in folderName else "ND"
            #print(ClausCountDet)
            clauseCount = folderName.split("clauseCount")[0].split(clausCountDet)[-1]
            #print(ClauseCount)
            clausLenDet = "DET" if "clauseCount_DET" in folderName else "ND"
            #print(ClausLenDet)
            clauseLen = folderName.split("clauseLength")[0].split(clausLenDet)[-1]
            #print(ClauseCount)
            SATstatus = folderName.split("_")[-1]
            #print(SATstatus)

            csv = "".join([SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","RAND,",str(round(np.mean(RANDresList),decimals)),",",str(round(np.std(RANDresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","MOMS,",str(round(np.mean(MOMSresList),decimals)),",",str(round(np.std(MOMSresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","JWOS,",str(round(np.mean(JWOSresList),decimals)),",",str(round(np.std(JWOSresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","JWTS,",str(round(np.mean(JWTSresList),decimals)),",",str(round(np.std(JWTSresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","DLIS,",str(round(np.mean(DLISresList),decimals)),",",str(round(np.std(DLISresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","DLCS,",str(round(np.mean(DLCSresList),decimals)),",",str(round(np.std(DLCSresList),decimals)),"\n"])
            
        else:
            csv = ""
        #TODO: print results for all cnfs?

        #print("done")
        return(csv)


# function to process files in multiple folders at once
def mutipleHeuristicComp(path):
    folders = os.listdir(path)

    #print(folders)

    if len(folders)==0:
        print("ERROR: folder is empty, pass a folder containing multiple folders with cnfs")
    else:
        outPath = "".join([path, "heuristicComparison.csv"])
        csvDat = open(outPath,"w+")
        csvDat.write("Satisfiability,Vars,ClauseCount,ClauseCountDet,ClauseLen,ClauseLenDet,Heuristic,AverageS,SD\n")
        for folder in folders:
            folderPath = "".join([path,folder,"/"])
            if os.path.isdir(folderPath):
                if len(os.listdir(folderPath))>1:
                    csv = heuristicsComp(folderPath)
                    csvDat.write(csv)
                    print("".join([folder," processed"]))
                else:
                    print("".join([folder," is empty! Continuing with next directory"]))
            else:
                print("".join(["ERROR processing ",folder,", it is not a folder! Continuing with next object"]))
        csvDat.write("")
        csvDat.close



def mutipleDPLLComp(path):
    folders = os.listdir(path)

    #print(folders)

    if len(folders)==0:
        print("ERROR: folder is empty, pass a folder containing multiple folders with cnfs")
    else:
        outPath = "".join([path, "DPLLComparison.csv"])
        csvDat = open(outPath,"w+")
        csvDat.write("Satisfiability,Vars,ClauseCount,ClauseCountDet,ClauseLen,ClauseLenDet,DPLLVariant,AverageS,SD\n")
        for folder in folders:
            folderPath = "".join([path,folder,"/"])
            if os.path.isdir(folderPath):
                if len(os.listdir(folderPath))>1:
                    csv = dpllComp(folderPath)
                    csvDat.write(csv)
                    print("".join([folder," processed"]))
                else:
                    print("".join([folder," is empty! Continuing with next directory"]))
            else:
                print("".join(["ERROR processing ",folder,", it is not a folder! Continuing with next object"]))
        csvDat.write("")
        csvDat.close
                