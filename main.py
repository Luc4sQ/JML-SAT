# Importing some stuff
import numpy as np
import src.input.args as arg
import src.input.dimacs as sid

# functioning code! returns a serious KNF
arguments = {"-dp", "-dpll"}
undefined = 0

specifiedArgument, path = arg.getArguments(arguments)

# first case: everything read properly
if path != undefined:
    KNF = sid.FileReader(path)
    
    # AND: the file was a legit dimacs file
    if KNF != undefined:

        ########## HERE is the main procedure place. ADD CODE HERE ########## 

        satisfiable = False
        
        print(KNF)
        
        print(satisfiable)

        #####################################################################

# second case: nothing, because no proper arguments supplied
else: 
    pass