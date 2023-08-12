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
positionTree = list()
# we define warning to be printed 
waringing = "warning: To make the visualisation possible the speed of the algorithm was slowed down substantially, it might therefore run for a very long time."

consideredLits = list()

# in this list we will save the strings representing the trees at the different time steps to plot them later using R
tree_seq = list()

def dpll_unit_visual_alg(cnf):
    global newcik_dict

    #print("positionTree at beginning",positionTree)
    # applying unit resolution first
    new_cnf, resolutedLiterals = unitResolution(cnf,[])
    #print("resolvents:",resolutedLiterals)
    print("writing:",positionTree,resolutedLiterals)
    if len(positionTree+resolutedLiterals)!=0:
        tree_seq.append("".join(["current literals = ",str(positionTree+[int(x) for x in resolutedLiterals])[1:-1],"\n\n"]))

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
        #print("positionTree updated",positionTree)

         # we update the dictionary used to plot the trees with the new information
        newcik_dict = update_dict(newcik_dict,positionTree)

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
        print("former writing",positionTree)
        #tree_seq.append("".join(["current literals = ",str(positionTree)[1:-1],"\n\n"]))
        # plot the actual tree in terminal
        tree = Phylo.read(handle, "newick")
        # will have to change this to also run on windows or linux
        #clearScreen()
        print(waringing)
        Phylo.draw_ascii(tree,column_width=80)
        time.sleep(0.75)

        # we need returned dpll literals, so we define them
        dpllOutput = dpll_unit_visual_alg(new_cond_cnf)


        #print("dpllOutput",dpllOutput)
        #print("dpllOutput[0]",dpllOutput[0])
        if dpllOutput[0] != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput[0]) | set(resolutedLiterals))
            #print("var:",var)
            #print("var_candidate",var_candidate)
            #print("dpllOutput[0]",dpllOutput[0])
            #print("resolutedLiterals",resolutedLiterals)
            return(var), tree_seq, consideredLits
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            consideredLits.append(-var_candidate)
            new_cond_cnf_neg = conditioning(new_cnf,-var_candidate)

            positionTree.pop()
            positionTree.append(-var_candidate)
            #print("positionTree updated",positionTree)
            newcik_dict = update_dict(newcik_dict,positionTree)
            newcik_dict_copy = copy.deepcopy(newcik_dict)
            #print("var cand",-var_candidate)
            #print("else",dicToNewick(newcik_dict_copy))

            # save the newick in our sequence
            tree_seq.append("".join(["(",dicToNewick(newcik_dict_copy),");\n"]))
            # add infomration about which was the last literal to be looked at to color the active brach of the search tree
            #tree_seq.append("".join(["latest literal = ",str(-int(var_candidate)),"\n\n"]))
            # add the currently tired variable combination
            print("former writing",positionTree)
            #tree_seq.append("".join(["current literals = ",str(positionTree)[1:-1],"\n\n"]))

            dpllOutput = dpll_unit_visual_alg(new_cond_cnf_neg)
            #print("dpllOutput",dpllOutput)
            #print("dpllOutput[0]",dpllOutput[0])
            if dpllOutput[0] != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput[0]) | set(resolutedLiterals))
                #print("var:",var)
                #print("var_candidate",var_candidate)
                #print("dpllOutput[0]",dpllOutput[0])
                #print("resolutedLiterals",resolutedLiterals)
                return(var), tree_seq, consideredLits
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                positionTree.pop()
                
                return "unsat", tree_seq, consideredLits


# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output(cnf,path):
    (output, tree_seq_list, consideredLits) = dpll_unit_visual_alg(cnf)
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
    #print(knf_variables_list)
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