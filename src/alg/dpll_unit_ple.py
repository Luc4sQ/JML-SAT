import numpy as np
import src.alg.dpll as dpll
from src.alg.dpll_unit import unitResolution

#######################################################################################################
########### FUNCTIONS USED IN DPLL WITH UNITRESOLUTION AND PURE LITERAL ELIMINATION ###################
#######################################################################################################

def pureLiteralElimination(cnf,litList):
    if not cnf:
        newCnf = cnf
        newLitList = litList
    else:
        # set a standard in case there are no pure literals and thus no new cnf is created
        newCnf = cnf
        newLitList = litList
        
        # generate a list containing all literals
        cnf_variables_list = np.unique(np.concatenate(cnf).ravel())
        
        # if the negation of a given literal in the list is not also in the list...
        for literal in cnf_variables_list:
            if -literal not in cnf_variables_list:
                litList.append(literal)
                newLitList = litList
                #print("pure",literal)
                newCnf = list()
                for clause in cnf:
                    if literal not in clause:
                        newCnf.append(clause)

        # if something was changed, run pure literal elimination again
        if newCnf != cnf:
            newCnf,newLitList = pureLiteralElimination(newCnf,newLitList)
                        
    return (newCnf,newLitList)

#######################################################################################################
########### DPLL ITSELF ADJUSTED WITH UNIT RESOLUTION #################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()

def dpll_alg_with_unit(cnf):

    # applying unit resolution first
    new_cnf, resolutedLiterals = unitResolution(cnf,[])
    new_cnf, resolutedLiterals = pureLiteralElimination(new_cnf, resolutedLiterals)
    #new_cnf, resolutedLiterals = pureLiteralElimination(cnf,[])

    # empty cnf is defined to be valid and therefore satisfiable
    if new_cnf == []:
        return resolutedLiterals
    
    # cnf containing empty clauses are by convention unsatisfiable
    elif dpll.checkIfEmpty(new_cnf):
        return "unsat"
    
    # If neither of these cases occour, we start to search the tree for satisfying variable assignments.
    # we do this recursively by repeatedly calling dpll_alg and assigning variables through conditioning
    # until one of the first two cases applies and the cnf is therefore either sat or unsat.
    else:
        # we first select the variable for conditioning 
        var_candidate = dpll.findMostCommonVar(new_cnf)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cond_cnf = dpll.conditioning(new_cnf,var_candidate)

        # we need returned dpll literals, so we define them
        dpllOutput = dpll_alg_with_unit(new_cond_cnf)

        if dpllOutput != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            new_cond_cnf_neg = dpll.conditioning(new_cnf,-var_candidate)
            dpllOutput = dpll_alg_with_unit(new_cond_cnf_neg)

            if dpllOutput != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                return "unsat"

# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output(cnf):
    output = dpll_alg_with_unit(cnf)
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
                variableAssignment.update({int(variable): False})
    return (satisfiability, variableAssignment)

