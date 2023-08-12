import numpy as np
from io import StringIO
import time
import os
from src.alg.dpll import conditioning, findMostCommonVar, checkIfEmpty, unitResolution, pureLiteralElimination

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

# This is the dpll algorithm with a few additions:
# the position list keeps track of whre we currently are in the tree, this is used to generate a dictionary that keeps
# track of the tree structure which is in turn used to generate a newick and plot the tree in the terminal.

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
        consideredLits.append(var_candidate)

        # then, we recursively search the different "layers" of the tree.
        # first for the conditioning on the non-negated variable:
        new_cnf = conditioning(cnf,var_candidate)

        position.append(var_candidate)

        # we update the dictionary used to plot the trees with the new information
        newcik_dict = update_dict(newcik_dict,position)

        ### plot the tree
        # first, copy the dictionary because it is edited during the translation to newick format
        newcik_dict_copy = copy.deepcopy(newcik_dict)
        # then translate it so newick and plot it using phylo of biopython
        handle = StringIO(dicToNewick(newcik_dict_copy))
        # save the newick in our sequence
        #tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))
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

            # save the newick in our sequence
            #tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))
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
def output_dpll_visual(cnf,path):
    (output, tree_seq_list, consideredLits) = dpll_visual_alg(cnf)

    # we first create a file and write the sequential tree data in it
    out_path = "".join([path.split(".")[0], "_dpll_tree.txt"])
    tree_dat = open(out_path,"w+")
    # write the number of variables, that will later be used to create a "sceleton" of the final tree
    knf_variables_list = np.array([])
    for array in cnf:
        for entry in array:
            if not abs(entry) in knf_variables_list:
                knf_variables_list = np.append(knf_variables_list,abs(entry))
    tree_dat.write("".join(["number of literals = ",str(len(knf_variables_list)),"\n\n"]))
    tree_dat.write("".join(["considered Literals: ", str(consideredLits)[1:-1],"\n\n"]))
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


#######################################################################################################
########### VISUAL DPLL WITH UNIT RESOLUTION ##########################################################
#######################################################################################################

# This is the dpll algorithm with a few additions:
# the position list keeps track of whre we currently are in the tree, this is used to generate a dictionary that keeps
# track of the tree structure which is in turn used to generate a newick and plot the tree in the terminal.
# Indipendently a list called positionTree is kept, this is used to write positional information, that also contains 
# updates that were due to unit resolution. This information is eventually written to a .txt file, which can be used
# to plot a prettier tree of the whole tree structure in R.

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()
newcik_dict = {}
positionTree = list()
consideredLits = list()

# in this list we will save the strings representing the trees at the different time steps to plot them later using R
tree_seq = list()

# List used to keep track of how many literals were choosen in the last step to make backtracking to the correct 
# literal possible in the visualisation. This is necessary becase we might need to make more than just one step 
# backwards if we assigned multiple variables due to Unit Resolution or Pure Literal Elimination
addedLits = [1]

def udpll_visual_alg(cnf):
    global newcik_dict
    global positionTree

    new_cnf, resolutedLiterals = unitResolution(cnf,[])
    #new_cnf, resolutedLiterals = pureLiteralElimination(cnf,[])

    # add infomration about which literals are being considered to plot the tree based on this
    # we take into account both the positinal information so far, that tells us where we were, and the
    # literals we got from the pure literal elimination
    if not positionTree:
        positionTree = [int(x) for x in resolutedLiterals]
    else:
        positionTree = positionTree+[int(x) for x in resolutedLiterals]
    
    # in order to backtrack and thereby add the positional information of the folowing steps in the right place,
    # we need to keep track of how many steps we made so we can go back
    # we overwrite the last variable assignment step in this list of steps with the number of literals + 1 since
    # ple happens before the next variable assignment, so this is one step!
    if not not resolutedLiterals:
        addedLits[-1]=(len(resolutedLiterals))+1
    if len(positionTree)!=0:
        tree_seq.append("".join(["current literals = ",str(positionTree)[1:-1],"\n\n"]))

    # empty cnf is defined to be valid and therefore satisfiable
    if new_cnf == []:
        return resolutedLiterals, tree_seq, consideredLits
    
    # cnf containing empty clauses are by convention unsatisfiable
    elif checkIfEmpty(new_cnf):
        return "unsat", tree_seq, consideredLits
    
    # If neither of these cases occour, we start to search the tree for satisfying variable assignments.
    # we do this recursively by repeatedly calling dpll_alg and assigning variables through conditioning
    # until one of the first two cases applies and the cnf is therefore either sat or unsat.
    else:
        # we first select the variable for conditioning 
        var_candidate = int(findMostCommonVar(new_cnf))

        consideredLits.append(var_candidate)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cond_cnf = conditioning(new_cnf,var_candidate)

        positionTree.append(var_candidate)
        addedLits.append(1)

        position.append(var_candidate)

        # we update the dictionary used to plot the trees with the new information
        newcik_dict = update_dict(newcik_dict,position)

        ### print the tree
        # first, copy the dictionary because it is edited during the translation to newick format
        newcik_dict_copy = copy.deepcopy(newcik_dict)
        # then translate it so newick and plot it using phylo of biopython
        handle = StringIO(dicToNewick(newcik_dict_copy))
        # save the newick in our sequence
        #tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))
        # plot the actual tree in terminal
        tree = Phylo.read(handle, "newick")
        clearScreen()
        print(waringing)
        Phylo.draw_ascii(tree,column_width=80)
        time.sleep(0.75)

        # we need returned dpll literals, so we define them
        dpllOutput = udpll_visual_alg(new_cond_cnf)

        if dpllOutput[0] != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput[0]) | set(resolutedLiterals))
            return(var), tree_seq, consideredLits
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            consideredLits.append(-var_candidate)
            new_cond_cnf_neg = conditioning(new_cnf,-var_candidate)

            #positionTree.pop()
            positionTree = positionTree[0:-addedLits[-1]]
            addedLits.pop()
            positionTree.append(-var_candidate)
            addedLits.append(1)

            position.pop()
            position.append(-var_candidate)
            newcik_dict = update_dict(newcik_dict,position)
            #newcik_dict_copy = copy.deepcopy(newcik_dict)

            # save the newick in our sequence
            #tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))

            dpllOutput = udpll_visual_alg(new_cond_cnf_neg)

            if dpllOutput[0] != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput[0]) | set(resolutedLiterals))
                return(var), tree_seq, consideredLits
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                positionTree = positionTree[0:-addedLits[-1]]
                addedLits.pop()

                position.pop()
                
                return "unsat", tree_seq, consideredLits


# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output_udpll_visual(cnf,path):
    (output, tree_seq_list, consideredLits) = udpll_visual_alg(cnf)
    # we first create a file and write the sequential tree data in it
    out_path = "".join([path.split(".")[0], "_udpll_tree.txt"])
    tree_dat = open(out_path,"w+")
    # write the number of variables, that will later be used to create a "sceleton" of the final tree
    knf_variables_list = np.array([])
    for array in cnf:
        for entry in array:
            if not abs(entry) in knf_variables_list:
                knf_variables_list = np.append(knf_variables_list,abs(entry))
    tree_dat.write("".join(["number of literals = ",str(len(knf_variables_list)),"\n\n"]))
    tree_dat.write("".join(["considered Literals: ", str(consideredLits)[1:-1],"\n\n"]))
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



#######################################################################################################
########### VISUAL DPLL WITH PURE LITERAL ELIMINATION #################################################
#######################################################################################################

# This is the dpll algorithm with a few additions:
# the position list keeps track of whre we currently are in the tree, this is used to generate a dictionary that keeps
# track of the tree structure which is in turn used to generate a newick and plot the tree in the terminal.
# Indipendently a list called positionTree is kept, this is used to write positional information, that also contains 
# updates that were due to pure literal elimination. This information is eventually written to a .txt file, which can 
# be used to plot a prettier tree of the whole tree structure in R.

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()
newcik_dict = {}
positionTree = list()
consideredLits = list()

# in this list we will save the strings representing the trees at the different time steps to plot them later using R
tree_seq = list()

# List used to keep track of how many literals were choosen in the last step to make backtracking to the correct 
# literal possible in the visualisation. This is necessary becase we might need to make more than just one step 
# backwards if we assigned multiple variables due to Unit Resolution or Pure Literal Elimination
addedLits = [1]

def dpllple_visual_alg(cnf):
    global newcik_dict
    global positionTree

    #new_cnf, resolutedLiterals = unitResolution(cnf,[])
    new_cnf, resolutedLiterals = pureLiteralElimination(cnf,[])

    # add infomration about which literals are being considered to plot the tree based on this
    # we take into account both the positinal information so far, that tells us where we were, and the
    # literals we got from the pure literal elimination
    if not positionTree:
        positionTree = [int(x) for x in resolutedLiterals]
    else:
        positionTree = positionTree+[int(x) for x in resolutedLiterals]
    
    # in order to backtrack and thereby add the positional information of the folowing steps in the right place,
    # we need to keep track of how many steps we made so we can go back
    # we overwrite the last variable assignment step in this list of steps with the number of literals + 1 since
    # ple happens before the next variable assignment, so this is one step!
    if not not resolutedLiterals:
        addedLits[-1]=(len(resolutedLiterals))+1
    if len(positionTree)!=0:
        tree_seq.append("".join(["current literals = ",str(positionTree)[1:-1],"\n\n"]))

    # empty cnf is defined to be valid and therefore satisfiable
    if new_cnf == []:
        return resolutedLiterals, tree_seq, consideredLits
    
    # cnf containing empty clauses are by convention unsatisfiable
    elif checkIfEmpty(new_cnf):
        return "unsat", tree_seq, consideredLits
    
    # If neither of these cases occour, we start to search the tree for satisfying variable assignments.
    # we do this recursively by repeatedly calling dpll_alg and assigning variables through conditioning
    # until one of the first two cases applies and the cnf is therefore either sat or unsat.
    else:
        # we first select the variable for conditioning 
        var_candidate = int(findMostCommonVar(new_cnf))

        consideredLits.append(var_candidate)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cond_cnf = conditioning(new_cnf,var_candidate)

        positionTree.append(var_candidate)
        addedLits.append(1)

        position.append(var_candidate)

        # we update the dictionary used to plot the trees with the new information
        newcik_dict = update_dict(newcik_dict,position)

        ### print the tree
        # first, copy the dictionary because it is edited during the translation to newick format
        newcik_dict_copy = copy.deepcopy(newcik_dict)
        # then translate it so newick and plot it using phylo of biopython
        handle = StringIO(dicToNewick(newcik_dict_copy))
        # save the newick in our sequence
        #tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))
        # plot the actual tree in terminal
        tree = Phylo.read(handle, "newick")
        clearScreen()
        print(waringing)
        Phylo.draw_ascii(tree,column_width=80)
        time.sleep(0.75)

        # we need returned dpll literals, so we define them
        dpllOutput = dpllple_visual_alg(new_cond_cnf)

        if dpllOutput[0] != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput[0]) | set(resolutedLiterals))
            return(var), tree_seq, consideredLits
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            consideredLits.append(-var_candidate)
            new_cond_cnf_neg = conditioning(new_cnf,-var_candidate)

            #positionTree.pop()
            positionTree = positionTree[0:-addedLits[-1]]
            addedLits.pop()
            positionTree.append(-var_candidate)
            addedLits.append(1)

            position.pop()
            position.append(-var_candidate)
            newcik_dict = update_dict(newcik_dict,position)
            #newcik_dict_copy = copy.deepcopy(newcik_dict)

            # save the newick in our sequence
            #tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))

            dpllOutput = dpllple_visual_alg(new_cond_cnf_neg)

            if dpllOutput[0] != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput[0]) | set(resolutedLiterals))
                return(var), tree_seq, consideredLits
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                positionTree = positionTree[0:-addedLits[-1]]
                addedLits.pop()

                position.pop()
                
                return "unsat", tree_seq, consideredLits


# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output_dpllple_visual(cnf,path):
    (output, tree_seq_list, consideredLits) = dpllple_visual_alg(cnf)
    # we first create a file and write the sequential tree data in it
    out_path = "".join([path.split(".")[0], "_dpllple_tree.txt"])
    tree_dat = open(out_path,"w+")
    # write the number of variables, that will later be used to create a "sceleton" of the final tree
    knf_variables_list = np.array([])
    for array in cnf:
        for entry in array:
            if not abs(entry) in knf_variables_list:
                knf_variables_list = np.append(knf_variables_list,abs(entry))
    tree_dat.write("".join(["number of literals = ",str(len(knf_variables_list)),"\n\n"]))
    tree_dat.write("".join(["considered Literals: ", str(consideredLits)[1:-1],"\n\n"]))
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

