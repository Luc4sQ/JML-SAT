import numpy as np
from io import StringIO
import time
import os
from src.alg.dpll import conditioning, findMostCommonVar, checkIfEmpty
from src.alg.dpll_unit import unitResolution
from src.alg.dpll_visual import update_dict, dicToNewick, clearScreen

# Bio is a package including Phylo, which can be used to plog phylogenetic trees.
# here it will be applied to plot decision trees.
from Bio import Phylo

# functions will be needed to update the maps used to plot the trees
from flatten_dict import flatten, unflatten
from mergedeep import merge
import copy


#######################################################################################################
########### VISUAL DPLL WITH UNIT RESOLUTION ##########################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()
newcik_dict = {}
position = list()
# we define warning to be printed 
waringing = "warning: To make the visualisation possible the speed of the algorithm was slowed down substantially, it might therefore run for a very long time."

def dpll_unit_visual_alg(cnf):
    global newcik_dict

    # applying unit resolution first
    new_cnf, resolutedLiterals = unitResolution(cnf,[])

    # empty cnf is defined to be valid and therefore satisfiable
    if new_cnf == []:
        return resolutedLiterals
    
    # cnf containing empty clauses are by convention unsatisfiable
    elif checkIfEmpty(new_cnf):
        return "unsat"
    
    # If neither of these cases occour, we start to search the tree for satisfying variable assignments.
    # we do this recursively by repeatedly calling dpll_alg and assigning variables through conditioning
    # until one of the first two cases applies and the cnf is therefore either sat or unsat.
    else:
        # we first select the variable for conditioning 
        var_candidate = findMostCommonVar(new_cnf)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cond_cnf = conditioning(new_cnf,var_candidate)

        position.append(var_candidate)

         # we update the dictionary used to plot the trees with the new information
        newcik_dict = update_dict(newcik_dict,position)

        ### print the tree
        # first, copy the dictionary because it is edited during the translation to newick format
        newcik_dict_copy = copy.deepcopy(newcik_dict)
        # then translate it so newick and plot it using phylo of biopython
        handle = StringIO(dicToNewick(newcik_dict_copy))
        tree = Phylo.read(handle, "newick")
        # will have to change this to also run on windows or linux
        clearScreen()
        print(waringing)
        Phylo.draw_ascii(tree,column_width=80)
        time.sleep(0.75)

        # we need returned dpll literals, so we define them
        dpllOutput = dpll_unit_visual_alg(new_cond_cnf)


        if dpllOutput != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            new_cond_cnf_neg = conditioning(new_cnf,-var_candidate)
            dpllOutput = dpll_unit_visual_alg(new_cond_cnf_neg)

            if dpllOutput != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                return "unsat"


# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output(cnf):
    output = dpll_unit_visual_alg(cnf)
    if output == "unsat":
        satisfiability = False
        variableAssignment = {}
    else:
        satisfiability = True
        variableAssignment = {}
        for variable in output:
            if variable > 0:
                variableAssignment.update({int(variable): True})
            else:
                variableAssignment.update({abs(int(variable)): False})
    return (satisfiability, variableAssignment)