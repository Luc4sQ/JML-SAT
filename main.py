# Importing some stuff
import numpy as np
import src.input.args as arg
import src.input.dimacs as sid
import src.input.generateCNF as genCNF
import src.alg.bruteforce as br
import src.timing.measure as ms
import src.timing.algComparison as comp
import src.alg.dpll as dpll
import src.alg.dp as dp
import src.alg.cdcl as cdcl
import src.timing.statistics as st

import src.alg.dpll_visual as dpll_visual

# functioning code! returns a serious KNF
ARGUMENTS = {"-bf", "-dpll","-dpll_visual", "-udpll", "-dpllple","-dpllple_visual", "-udpllple", "-udpll_visual", "-dp", "-DPLLcomp", "-HEURcomp", "-generateCNF","-multiHEURcomp","-multiHEURcomp_dpll","-multiDPLLcomp","-cdcl"}
UNDEFINED = 0

specifiedArgument, path = arg.getArguments(ARGUMENTS)

# first case: everything read properly
if path != UNDEFINED:

    try:
        KNF, properties = sid.FileReader(path)
    except:
        data = st.makeMultipleKNFs(path, specifiedArgument)
        values = st.reportStatistics(data)
        print("standard deviation: ",values[1], " and mean: ",values[0])
        exit()
    
    # also check weather a comparison of algorithms should be done since the path specified will then be for folder not files
    if specifiedArgument not in ["-DPLLcomp","-HEURcomp","-generateCNF","-multiHEURcomp","-multiDPLLcomp","-multiHEURcomp_dpll"]:
        KNF, properties = sid.FileReader(path)
    
        # AND: the file was a legit dimacs file
        if KNF != UNDEFINED:

            if specifiedArgument == "-cdcl":
                var = list()
                print(KNF)
                time, output = ms.timeInSeconds(cdcl.cdcl, (KNF,properties))

                satisfiable = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:"," not implemented yet")
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")



            # Initiate DPLL if parameter -dpll was given
            if specifiedArgument == "-dpll":
                var = list()
                time, output = ms.timeInSeconds(dpll.output_dpll, KNF)

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")
            
            # Initiate the visualised version of DPLL if parameter -dpll_visual was given
            if specifiedArgument == "-dpll_visual":
                var = list()

                (satisfiable,variableAssignment)=dpll_visual.output_dpll_visual(KNF,path)

                if satisfiable:
                    print(satisfiable, "\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable)


            # Initiate DPLL with unit resolution if parameter -udpll was given
            if specifiedArgument == "-udpll":
                var = list()

                time, output = ms.timeInSeconds(dpll.output_udpll, KNF)

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")
            
            
            # Initiate DPLL with pure literal elimination if parameter -dpllple was given
            if specifiedArgument == "-dpllple":
                var = list()

                time, output = ms.timeInSeconds(dpll.output_dpllple, KNF)

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")
            
            # Initiate DPLL with unit resolution and pure literal elimination if parameter -udpllple was given
            if specifiedArgument == "-udpllple":
                var = list()

                time, output = ms.timeInSeconds(dpll.output_udpllple, KNF)

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")


            # Initiate the visualised version of DPLL with unit resolution if parameter -udpll_visual was given
            if specifiedArgument == "-udpll_visual":
                var = list()

                (satisfiable,variableAssignment)=dpll_visual.output_udpll_visual(KNF,path)

                if satisfiable:
                    print(satisfiable, "\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable)

            # Initiate the visualised version of DPLL with pure literal elimination if parameter -udpll_visual was given
            if specifiedArgument == "-dpllple_visual":
                var = list()

                (satisfiable,variableAssignment)=dpll_visual.output_dpllple_visual(KNF,path)

                if satisfiable:
                    print(satisfiable, "\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable)


            
            # Initiate brute force if parameter -bf was given
            if specifiedArgument == "-bf":

                time, output = ms.timeInSeconds(br.bruteForce, (KNF, properties))

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")


            if specifiedArgument == "-dp":

                time, output = ms.timeInSeconds(dp.backtrack, (KNF, properties))

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")


    if specifiedArgument == "-DPLLcomp":

            comp.dpllComp(path)


    if specifiedArgument == "-multiDPLLcomp":

            comp.mutipleDPLLComp(path)


    if specifiedArgument == "-HEURcomp":

            comp.heuristicsComp(path)


    if specifiedArgument == "-multiHEURcomp":

            comp.mutipleHeuristicComp(path,"udpll")

            
    if specifiedArgument == "-multiHEURcomp_dpll":
            
            comp.mutipleHeuristicComp(path,"dpll")
            

    if specifiedArgument == "-generateCNF":

            genCNF.multipleCNFs(path)
            

# second case: nothing, because no proper arguments supplied
else: 
    pass