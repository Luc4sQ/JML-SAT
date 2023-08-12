# Importing some stuff
import numpy as np
import src.input.args as arg
import src.input.dimacs as sid
import src.input.generateCNF as genCNF
import src.alg.bruteforce as br
import src.timing.measure as ms
import src.timing.algComparison as comp
import src.alg.dpll as dpll
import src.alg.dpll_unit as udpll
import src.alg.dpll_unit_ple as pledpll
import src.alg.dp as dp
import src.alg.dpll_visual as dpll_visual
import src.alg.dpll_unit_visual as udpll_visual

# functioning code! returns a serious KNF
ARGUMENTS = {"-bf", "-dpll","-dpll_visual", "-udpll", "-udpllple", "-udpll_visual", "-dp", "-DPLLcomp", "-HEURcomp", "-generateCNF"}
UNDEFINED = 0

specifiedArgument, path = arg.getArguments(ARGUMENTS)

# first case: everything read properly
if path != UNDEFINED:
    
    # also check weather a comparison of algorithms should be done since the path specified will then be for folder not files
    if specifiedArgument not in ["-DPLLcomp","-HEURcomp","-generateCNF"]:
        KNF, properties = sid.FileReader(path)
    
        # AND: the file was a legit dimacs file
        if KNF != UNDEFINED:

            # Initiate DPLL if parameter -dpll was given
            if specifiedArgument == "-dpll":
                var = list()

                time, output = ms.timeInSeconds(dpll.output, KNF)

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")
            
            # Initiate the visualised version of DPLL if parameter -dpll_visual was given
            if specifiedArgument == "-dpll_visual":
                var = list()

                (satisfiable,variableAssignment)=dpll_visual.output(KNF,path)

                if satisfiable:
                    print(satisfiable, "\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable)

            """""
            ##### OOOLLLDLDDDDDd
            # Initiate the visualised version of DPLL if parameter -dpll_visual was given
            if specifiedArgument == "-dpll_visual":
                var = list()

                (satisfiable,variableAssignment)=dpll_visual.output(KNF)

                if satisfiable:
                    print(satisfiable, "\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable)
            """


            # Initiate DPLL with unit resolution if parameter -udpll was given
            if specifiedArgument == "-udpll":
                var = list()

                time, output = ms.timeInSeconds(udpll.output, KNF)

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")
            
            
            # Initiate DPLL with unit resolution if parameter -udpllple was given
            if specifiedArgument == "-udpllple":
                var = list()

                time, output = ms.timeInSeconds(pledpll.output, KNF)

                satisfiable, variableAssignment = output

                if satisfiable:
                    print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
                else:
                    print(satisfiable, f"in {time:.5f} Sekunden!")


            # Initiate the visualised version of DPLL with unit resolution if parameter -udpll_visual was given
            if specifiedArgument == "-udpll_visual":
                var = list()

                (satisfiable,variableAssignment)=udpll_visual.output(KNF,path)

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

            #comp.dpllComp(path)
            comp.mutipleDPLLComp(path)

    if specifiedArgument == "-HEURcomp":

            #comp.heuristicsComp(path)
            comp.mutipleHeuristicComp(path)

    if specifiedArgument == "-generateCNF":

            #genCNF.output(path)
            genCNF.runTests(path)
            

# second case: nothing, because no proper arguments supplied
else: 
    pass