# Importing some stuff
import numpy as np
import os
import src.input.dimacs as sid
import src.timing.measure as ms
import src.alg.dpll as dpll


#######################################################################################################
########### DPLL, uDPLL AND uDPLLple ##################################################################
#######################################################################################################

# compare the multiple versions of dpll based on files in a given folder
def dpllComp(path):

    # if the files in the folder were written by this program, we can extract information from the folder name
    selfGeneratedCNF = True

    # TODO: if no CNFs are in folder, print error
    if not path.endswith("/"):
        print("ERROR: path for a folder with CNFs needs to be provided")
        
    else:

        out_path = "".join([path, "SATstats_dpll.txt"])
        stats_dat = open(out_path,"w+")

        # TODO: add info about System test was run on, date and time, ...

        files = os.listdir(path)

        # create control points at which a status update will be printed in the terminal (if more than 20 formulas are in folder)
        stepCount = 50
        controlPoints = np.array([])
        if len(files) >= stepCount:
            for j in range(1,stepCount):
                controlPoints = np.append(controlPoints,files[j*round(len(files)/stepCount)])

        # define the empty arrays in which the stats will be written during the actual measurements
        DPLLresList = np.array([])
        uDPLLresList = np.array([])
        DPLLpleresList = np.array([])
        uDPLLpleresList = np.array([])

        # keep track of how many files were considered and how many were satisfiable 
        SATcount = 0
        CNFcount = 0

        # iterativeley measure time it took to determine satisfiablilty for each of the algorythms
        for file in files:

            if file.endswith("cnf"):

                CNFcount = CNFcount + 1

                # extract cnf
                wholePath = "".join([path,file])
                cnf, properties = sid.FileReader(wholePath)

                # run the different versions of dpll on the specified files

                timeDPLL, (satisfiableDPLL, variableAssignment) = ms.timeInSeconds(dpll.output_dpll, cnf)

                timeUDPLL, (satisfiableUDPLL, variableAssignment) = ms.timeInSeconds(dpll.output_udpll, cnf)

                timeDPLLple, (satisfiableDPLLple, variableAssignment) = ms.timeInSeconds(dpll.output_dpllple, cnf)

                timeUDPLLple, (satisfiableUDPLLple, variableAssignment) = ms.timeInSeconds(dpll.output_udpllple, cnf)

                # test weather we got different results for satisfiability for the various versions and print error message if so
                if not satisfiableDPLL == satisfiableUDPLL and satisfiableDPLL == satisfiableUDPLLple and satisfiableDPLL == satisfiableDPLLple:
                    print("ERROR: file",file,"resulted in different SAT results: DPLL:",satisfiableDPLL,"uDPLL:",satisfiableUDPLL,"uDPLLple:",satisfiableUDPLLple)
                else:
                    # append the results to the respective lists of results
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
            varNum = folderName.split("vars")[0]
            clausCountDet = "DET" if "vars_DET" in folderName else "ND"
            clauseCount = folderName.split("clauseCount")[0].split(clausCountDet)[-1]
            clausLenDet = "DET" if "clauseCount_DET" in folderName else "ND"
            clauseLen = folderName.split("clauseLength")[0].split(clausLenDet)[-1]
            SATstatus = folderName.split("_")[-1]

            csv = "".join([SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","DPLL,",str(round(np.mean(DPLLresList),decimals)),",",str(round(np.std(DPLLresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","uDPLL,",str(round(np.mean(uDPLLresList),decimals)),",",str(round(np.std(uDPLLresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","DPLLple,",str(round(np.mean(DPLLpleresList),decimals)),",",str(round(np.std(DPLLpleresList),decimals)),"\n",
                        SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","uDPLLple,",str(round(np.mean(uDPLLpleresList),decimals)),",",str(round(np.std(uDPLLpleresList),decimals)),"\n"])
            
        else:
            csv = ""

        return(csv)


def heuristicsComp(path,dpllVariant):

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

            if file.endswith("cnf"):

                CNFcount = CNFcount + 1

                # extract cnf
                wholePath = "".join([path,file])
                cnf, properties = sid.FileReader(wholePath)

                # choose weather to run the tests with dpll or udpll based on what was specified
                alg = dpll.output_dpll if dpllVariant == "dpll" else dpll.output_udpll

                timeRAND, (satisfiableRAND, variableAssignment) = ms.timeInSecondsHeuristics(alg, cnf, "RAND")
                timeMOMS, (satisfiableMOMS, variableAssignment) = ms.timeInSecondsHeuristics(alg, cnf, "MOMS")
                timeJWOS, (satisfiableJWOS, variableAssignment) = ms.timeInSecondsHeuristics(alg, cnf, "JWOS")
                timeJWTS, (satisfiableJWTS, variableAssignment) = ms.timeInSecondsHeuristics(alg, cnf, "JWTS")
                timeDLCS, (satisfiableDLCS, variableAssignment) = ms.timeInSecondsHeuristics(alg, cnf, "DLCS")
                timeDLIS, (satisfiableDLIS, variableAssignment) = ms.timeInSecondsHeuristics(alg, cnf, "DLIS")

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
        stats_dat.write("".join(["Comparison of",dpllVariant,"with different search heuristics \n\n"]))
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
            varNum = folderName.split("vars")[0]
            clausCountDet = "DET" if "vars_DET" in folderName else "ND"
            clauseCount = folderName.split("clauseCount")[0].split(clausCountDet)[-1]
            clausLenDet = "DET" if "clauseCount_DET" in folderName else "ND"
            clauseLen = folderName.split("clauseLength")[0].split(clausLenDet)[-1]
            SATstatus = folderName.split("_")[-1]

            csv = "".join([dpllVariant,",",SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","RAND,",str(round(np.mean(RANDresList),decimals)),",",str(round(np.std(RANDresList),decimals)),"\n",
                        dpllVariant,",",SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","MOMS,",str(round(np.mean(MOMSresList),decimals)),",",str(round(np.std(MOMSresList),decimals)),"\n",
                        dpllVariant,",",SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","JWOS,",str(round(np.mean(JWOSresList),decimals)),",",str(round(np.std(JWOSresList),decimals)),"\n",
                        dpllVariant,",",SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","JWTS,",str(round(np.mean(JWTSresList),decimals)),",",str(round(np.std(JWTSresList),decimals)),"\n",
                        dpllVariant,",",SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","DLIS,",str(round(np.mean(DLISresList),decimals)),",",str(round(np.std(DLISresList),decimals)),"\n",
                        dpllVariant,",",SATstatus,",",varNum,",",clauseCount,",",clausCountDet,",",clauseLen,",",clausLenDet,",","DLCS,",str(round(np.mean(DLCSresList),decimals)),",",str(round(np.std(DLCSresList),decimals)),"\n"])
            
        else:
            csv = ""

        return(csv)


# function to process files in multiple folders at once
def mutipleHeuristicComp(path,dpllVariant):

    # generate list of all the folders
    folders = os.listdir(path)

    if len(folders)==0:
        print("ERROR: folder is empty, pass a folder containing multiple folders with cnfs")
    else:
        # generate a csv file the summary of the comparison will be written to
        outPath = "".join([path, "heuristicComparison_",dpllVariant,".csv"])
        csvDat = open(outPath,"w+")
        csvDat.write("dpllVariant,Satisfiability,Vars,ClauseCount,ClauseCountDet,ClauseLen,ClauseLenDet,Heuristic,AverageS,SD\n")
        
        # run tests on the files in each of the folders and write summarizing info to the csv
        for folder in folders:
            folderPath = "".join([path,folder,"/"])
            if os.path.isdir(folderPath):
                if len(os.listdir(folderPath))>1:
                    csv = heuristicsComp(folderPath,dpllVariant)
                    csvDat.write(csv)
                    print("".join([folder," processed"]))
                else:
                    print("".join([folder," is empty! Continuing with next directory"]))
            else:
                print("".join(["ERROR processing ",folder,", it is not a folder! Continuing with next object"]))
        csvDat.write("")
        csvDat.close


# function to process files in multiple folders at once
def mutipleDPLLComp(path):

    # generate list of all the folders
    folders = os.listdir(path)

    if len(folders)==0:
        print("ERROR: folder is empty, pass a folder containing multiple folders with cnfs")
    else:
        # generate a csv file the summary of the comparison will be written to
        outPath = "".join([path, "DPLLComparison.csv"])
        csvDat = open(outPath,"w+")
        csvDat.write("Satisfiability,Vars,ClauseCount,ClauseCountDet,ClauseLen,ClauseLenDet,DPLLVariant,AverageS,SD\n")
        # run tests on the files in each of the folders and write summarizing info to the csv
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
                