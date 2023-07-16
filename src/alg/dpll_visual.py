import numpy as np
from io import StringIO
import time
import os
from src.alg.dpll import conditioning, findMostCommonVar, checkIfEmpty

# Bio is a package including Phylo, which can be used to plog phylogenetic trees.
# here it will be applied to plot decision trees.
from Bio import Phylo

# functions will be needed to update the maps used to plot the trees
from flatten_dict import flatten, unflatten
from mergedeep import merge
import copy



#######################################################################################################
########### NECESSARY FUNCTIONS #######################################################################
#######################################################################################################

# function that updates the dictionary 
def update_dict(dictionary:dict,position:list):
    do_nothing_more = False
    flat_dict = flatten(dictionary)
    new_var = position[-1]
    key = tuple(position[:-1])
    if not key:
        flat_dict.update({new_var:0})
        dict = flat_dict
    else:
        # if we look at the negation of a variable we have considered before, the original form must have been unsat
        for i in range(0,len(flat_dict.keys())):
            if (not do_nothing_more): 
                difference = len(list(flat_dict.keys())[i])-len(position)
            if (not do_nothing_more and difference > 0):
                # we want to overwrite old entries so we unflatten
                intermediate_dict = unflatten(flat_dict)
                unflat_new_entry = unflatten({tuple(key+ (-new_var,)):"unsat",tuple(key+ (new_var,)):new_var})
                merge(intermediate_dict,unflat_new_entry)
                flat_dict = flatten(intermediate_dict)
                # name needs to be added after unflattening because otherwise the name is interpreted as a dictionary
                # still causes issues because the unflat meghod in the following steps messes things up
                do_nothing_more = True
                
        if (tuple(key + (-new_var,)) in flat_dict.keys() and not do_nothing_more):
            new_entry = {tuple(key + (-new_var,)):"unsat",tuple(key + (new_var,)):new_var}
            flat_dict.update(new_entry)
        # we deleate the entries at wich we want the tree to fork and repalce this position with dictionaries instead
        
        elif (tuple(position[:-2]) != () and tuple(position[:-2]) in flat_dict.keys() and not do_nothing_more):  
            del flat_dict[tuple(position[:-2])]
            flat_dict.update({key:new_var})
        
        elif (not do_nothing_more):   
            flat_dict.update({key:new_var})
        
        dict = unflatten(flat_dict)
    return dict


def dicToNewick(dictionary:dict):
    key0 = list(dictionary.keys())[0]
    value0 = dictionary.get(key0)

    if (len(dictionary.keys())==1):

        if (isinstance(value0,dict)):
            new_entry = dicToNewick(value0)
            dictionary.update({key0:new_entry})
            newick = dicToNewick(dictionary)
        else:
            newick = f"(({value0}){key0},{-key0})"

    elif (len(dictionary.keys())>1):
        key1 = list(dictionary.keys())[1]
        value1 = dictionary.get(key1)
        if (isinstance(value1,dict)):
            new_entry = dicToNewick(value1)
            dictionary.update({key1:new_entry})
            newick = dicToNewick(dictionary)
        else:
            newick = f"(({value0}){key0},({value1}){key1})"

    return newick

# clear screen comment depending on the operating system
def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

waringing = "warning: To make the visualisation possible the speed of the algorithm was slowed down substantially, it might therefore run for a very long time."

#######################################################################################################
########### VISUAL DPLL ITSELF ###############################################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()
newcik_dict = {}
position = list()

def dpll_visual_alg(cnf):

    global newcik_dict
    # empty cnf is defined to be valid and therefore satisfiable
    if cnf == []:
        return list()
    # cnf containing empty clauses are by convention unsatisfiable
    elif checkIfEmpty(cnf):
        return "unsat"
    
    # If neither of these cases occour, we start to search the tree for satisfying variable assignments.
    # we do this recursively by repeatedly calling dpll_visual_alg and assigning variables through conditioning
    # until one of the first two cases applies and the cnf is therefore either sat or unsat.
    else:
        # we first select the variable for conditioning 
        var_candidate = findMostCommonVar(cnf)

        # then, we recursively search the different "layers" of the tree.
        # first for the conditioning on the non-negated variable:
        new_cnf = conditioning(cnf,var_candidate)

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

        if dpll_visual_alg(new_cnf) != "unsat":
            var.append(var_candidate)
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:

            new_cnf_neg = conditioning(cnf,-var_candidate)
            
            position.pop()
            position.append(-var_candidate)
            newcik_dict = update_dict(newcik_dict,position)
            
            if dpll_visual_alg(new_cnf_neg) != "unsat":
                var.append(-var_candidate)
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                position.pop()
                return "unsat"

# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output(cnf):
    output = dpll_visual_alg(cnf)
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
    return satisfiability, variableAssignment






