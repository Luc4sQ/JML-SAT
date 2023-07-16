# Importing some stuff
import numpy as np
import src.input.args as arg
import src.input.dimacs as sid
import src.alg.bruteforce as br
import src.timing.measure as ms
import src.alg.dpll as dpll
import src.alg.dpll_unit as udpll
import src.alg.dp as dp
import src.alg.dpll_visual as dpll_visual

# functioning code! returns a serious KNF
ARGUMENTS = {"-bf", "-dpll","-dpll_visual", "-udpll", "-dp"}
UNDEFINED = 0

specifiedArgument, path = arg.getArguments(ARGUMENTS)

# first case: everything read properly
if path != UNDEFINED:
    KNF, properties = sid.FileReader(path)
    
    # AND: the file was a legit dimacs file
    if KNF != UNDEFINED:

        if specifiedArgument == "-udpll":
            var = list()

            time, output = ms.timeInSeconds(udpll.output, KNF)

            satisfiable, variableAssignment = output

            if satisfiable:
                print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
            else:
                print(satisfiable, f"in {time:.5f} Sekunden!")

        # Initiate DPLL if parameter -dpll was given
        if specifiedArgument == "-dpll":
            var = list()

            time, output = ms.timeInSeconds(dpll.output, KNF)

            satisfiable, variableAssignment = output

            if satisfiable:
                print(satisfiable, f"in {time:.5f} Sekunden!","\nThe following variable assignment satisfies input cnf:",variableAssignment)
            else:
                print(satisfiable, f"in {time:.5f} Sekunden!")
        
        # Initiate the visualized version of DPLL if parameter -dpll_visual was given
        if specifiedArgument == "-dpll_visual":
            var = list()

            time, output = ms.timeInSeconds(dpll_visual.output,KNF)

            if satisfiable:
                print(satisfiable, "\n The following variable assignment satisfies input cnf:",variableAssignment)
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


# second case: nothing, because no proper arguments supplied
else: 
    pass