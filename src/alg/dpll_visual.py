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

# Matolotlib is necessary to generate the pictures of the trees
import matplotlib as plt



#######################################################################################################
########### NECESSARY FUNCTIONS #######################################################################
#######################################################################################################

# function that updates the dictionary 
def update_dict(dictionary:dict,position:list):
    do_nothing_more = False
    flat_dict = flatten(dictionary)
    new_var = position[-1]
    key = tuple(position[:-1])
    print("key",key)
    if not key and not flat_dict:
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

                # first take care of case where we backtracked all the way to the first variable.
                # here, we can not simply the variable we are trying as a new value because we have no key.
                # instead what we first defined as the new variable is actually the new key and we assign it variable 0 as a placeholder
                if not key:
                    keyToAdd = np.array([int(new_var)])
                    new_varToAdd = 0
                    print("new entry",{tuple(np.array([-new_var])):"unsat",tuple(keyToAdd+ (new_varToAdd,)):new_varToAdd})
                    unflat_new_entry = unflatten({tuple(np.array([-new_var])):"unsat",tuple(keyToAdd+ (new_varToAdd,)):new_varToAdd})
                
                else:
                    unflat_new_entry = unflatten({tuple(key+ (-new_var,)):"unsat",tuple(key+ (new_var,)):new_var})
                merge(intermediate_dict,unflat_new_entry)
                flat_dict = flatten(intermediate_dict)
                # name needs to be added after unflattening because otherwise the name is interpreted as a dictionary
                # still causes issues because the unflat method in the following steps messes things up
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

def update_dict_fullTree(dictionary:dict,position:list):
    do_nothing_more = False
    flat_dict = flatten(dictionary)
    new_var = position[-1]
    key = tuple(position[:-1])
    if not key:
        flat_dict.update({new_var:0})
        dict = flat_dict
    else:
        # if we look at the negation of a variable we have considered before, the original form must have been unsat
        """"
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
                # still causes issues because the unflat method in the following steps messes things up
                do_nothing_more = True
        """
                
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
            newick = f"({value0}){key0},{-key0}"

    elif (len(dictionary.keys())>1):
        key1 = list(dictionary.keys())[1]
        value1 = dictionary.get(key1)
        if (isinstance(value1,dict)):
            new_entry = dicToNewick(value1)
            dictionary.update({key1:new_entry})
            newick = dicToNewick(dictionary)
        else:
            newick = f"({value0}){key0},({value1}){key1}"

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
consideredLits = list()

# in this list we will save the strings representing the trees at the different time steps to plot them later using R
tree_seq = list()

def dpll_visual_alg(cnf):

    global newcik_dict
    # empty cnf is defined to be valid and therefore satisfiable
    if cnf == []:
        return list(), tree_seq, consideredLits
    # cnf containing empty clauses are by convention unsatisfiable
    elif checkIfEmpty(cnf):
        return "unsat", tree_seq, consideredLits
    
    # If neither of these cases occour, we start to search the tree for satisfying variable assignments.
    # we do this recursively by repeatedly calling dpll_visual_alg and assigning variables through conditioning
    # until one of the first two cases applies and the cnf is therefore either sat or unsat.
    else:
        # we first select the variable for conditioning 
        var_candidate = int(findMostCommonVar(cnf))
        #var_candidate = cnf[0][0]
        print("var cand",var_candidate)
        consideredLits.append(var_candidate)

        # then, we recursively search the different "layers" of the tree.
        # first for the conditioning on the non-negated variable:
        new_cnf = conditioning(cnf,var_candidate)

        position.append(var_candidate)
        print("position",position)

        # we update the dictionary used to plot the trees with the new information
        newcik_dict = update_dict(newcik_dict,position)

        ### print the tree
        # first, copy the dictionary because it is edited during the translation to newick format
        newcik_dict_copy = copy.deepcopy(newcik_dict)
        # then translate it so newick and plot it using phylo of biopython
        handle = StringIO(dicToNewick(newcik_dict_copy))
        # save the newick in our sequence
        tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))
        # add infomration about which was the last literal to be looked at to color the active brach of the search tree
        #tree_seq.append("".join(["latest literal = ",str(int(var_candidate)),"\n\n"]))
        # add the currently tired variable combination
        tree_seq.append("".join(["current literals = ",str(position)[1:-1],"\n\n"]))
        # plot the actual tree in terminal
        tree = Phylo.read(handle, "newick")
        # will have to change this to also run on windows or linux
        clearScreen()
        print(waringing)
        Phylo.draw_ascii(tree,column_width=80)
        print(dicToNewick(newcik_dict_copy))
        time.sleep(0.75)

        if dpll_visual_alg(new_cnf)[0] != "unsat":
            var.append(var_candidate)
            return(var), tree_seq, consideredLits
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            consideredLits.append(-var_candidate)
            new_cnf_neg = conditioning(cnf,-var_candidate)
            
            position.pop()
            position.append(-var_candidate)
            newcik_dict = update_dict(newcik_dict,position)
            newcik_dict_copy = copy.deepcopy(newcik_dict)
            print("var cand",-var_candidate)
            print("else",dicToNewick(newcik_dict_copy))

            # save the newick in our sequence
            tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))
            # add infomration about which was the last literal to be looked at to color the active brach of the search tree
            #tree_seq.append("".join(["latest literal = ",str(-int(var_candidate)),"\n\n"]))
            # add the currently tired variable combination
            tree_seq.append("".join(["current literals = ",str(position)[1:-1],"\n\n"]))
            
            if dpll_visual_alg(new_cnf_neg)[0] != "unsat":
                var.append(-var_candidate)
                return(var), tree_seq, consideredLits
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                position.pop()
                return "unsat", tree_seq, consideredLits


# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output(cnf,path):
    (output, tree_seq_list, consideredLits) = dpll_visual_alg(cnf)

    # we first create a file and write the sequential tree data in it
    out_path = "".join([path.split(".")[0], "_tree.txt"])
    tree_dat = open(out_path,"w+")
    # write the number of variables, that will later be used to create a "sceleton" of the final tree
    knf_variables_list = np.array([])
    for array in cnf:
        for entry in array:
            if not abs(entry) in knf_variables_list:
                knf_variables_list = np.append(knf_variables_list,abs(entry))
    tree_dat.write("".join(["number of literals = ",str(len(knf_variables_list)),"\n\n"]))
    tree_dat.write("".join(["considered Literals: ", str(consideredLits)[1:-1],"\n\n"]))
    print(knf_variables_list)
    # if satisfiable add the number of literals that were used to find sat assignment at inner node
    if isinstance(output,list):
        tree_dat.write("".join(["SAT","\n\n", "number of literals necessary to find assignment =",str(len(output)),"\n\n"]))
    else:
        tree_dat.write("UNSAT \n\n")
    # add the sequential tree data to the file
    for i in range(len(tree_seq_list)):
        tree_dat.write(tree_seq_list[i])
    tree_dat.close()

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



