# Importing some stuff
import src.input.args as arg
import src.input.dimacs as sid

# functioning code! returns a serious KNF

arguments = {"-dp", "-dpll"}

specifiedArgument, path = arg.getArguments(arguments)

# first case: everything read properly
if path != 0:
    KNF = sid.FileReader(path)
    
    if KNF != 0:

        ########## HERE is the main procedure place. ADD CODE HERE ########## 

        satisfiable = False
        
        print(KNF)

        print(satisfiable)

        #####################################################################

# second case: just exact one argument got supplied
elif specifiedArgument != 0:
    print("the current algorithm is: "+specifiedArgument+".\nplease add a PATH or type --help as an argument")

# last case: nothing, because no proper arguments supplied
else: 
    pass