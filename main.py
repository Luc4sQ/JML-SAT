# Importing some stuff
import numpy as np
import src.input.args as arg
import src.input.dimacs as sid
import src.alg.bruteforce as br
import src.timing.measure as ms

# functioning code! returns a serious KNF
ARGUMENTS = {"-bf","-dp", "-dpll"}
UNDEFINED = 0

specifiedArgument, path = arg.getArguments(ARGUMENTS)

# first case: everything read properly
if path != UNDEFINED:
    KNF, properties = sid.FileReader(path)
    
    # AND: the file was a legit dimacs file
    if KNF != UNDEFINED:

        ########## HERE is the main procedure place. ADD CODE HERE ########## 

        satisfiable = False
        
        #print(KNF)
        
        if specifiedArgument == "-bf":

            time, satisfiable = ms.timeInSeconds(br.bruteForce, (KNF, properties))
            print(satisfiable, f"in {time:.5f} Sekunden!")


        #####################################################################

# second case: nothing, because no proper arguments supplied
else: 
    pass