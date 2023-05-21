import numpy as np
import src.alg.dpll as dpll

#######################################################################################################
########### FUNCTIONS USED IN DPLL WITH UNITRESOLUTION ################################################
#######################################################################################################

def unitResolution(cnf,list):
    # returning of the unitresolution doesnt do anything
    if not cnf:
        return (cnf,list)
    else:
        for disjunction in cnf:
            # recursively implementing unit resolution by using conditioning of dpll file
            if len(disjunction) == 1:
                new_cnf = dpll.conditioning(cnf,disjunction)
                new_list = list
                new_list.append(float(disjunction))
                new_cnf, new_list = unitResolution(new_cnf,new_list)
                return (new_cnf,new_list)
            
    return (cnf,list)

#######################################################################################################
########### DPLL ITSELF ADJUSTED WITH UNIT RESOLUTION #################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()

def dpll_alg_with_unit(cnf):
    # applying unit resolution first
    new_cnf, resolutedLiterals = unitResolution(cnf,[])

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

