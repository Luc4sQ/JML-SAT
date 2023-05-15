import numpy as np

#######################################################################################################
########### FUNCTIONS USED IN DPLL ####################################################################
#######################################################################################################

# simplify the cnf by assigning one of the variable to true or false and deleating clauses and literals 
def conditioning(cnf,var):
    new_cnf = list()
    for entry in cnf:
        if (len(entry)==0):
            new_cnf.append(np.array([]))
        elif var not in entry:
            if -var in entry:
                index = np.argwhere(entry==-var)
                new_entry = np.delete(entry,index)
                new_cnf.append(new_entry)
            else:
                new_cnf.append(entry)  
    return new_cnf

# find the most variables occouring most often across al clauses 
def findMostCommonVar(cnf):
    # create an array containing all the variables as often as they occour in the clauses (in either negated and non-negated state)
    knf_variables_list = np.array([])
    for array in cnf:
        for entry in array:
            knf_variables_list = np.append(knf_variables_list,abs(entry))
    # count the occourance of the variables
    knf_variables_counts = np.unique(knf_variables_list, return_counts=True)
    # and choose the most frequent one
    var = np.select(knf_variables_counts[1]==np.max(knf_variables_counts[1]),knf_variables_counts[0]).item()
    # TODO: if we will not end up picking the variables in a different way anyways, it would make sense to also check weather the negated
    # or the non-negated form are more common and pick that as the variable.
    return var

# since it can't simply be checked, weather an empty array is in a list (empty arrays are assigned a truth value by default), this function checks it
def checkIfEmpty(cnf):
    empty = False
    for element in cnf:
        if len(element)==0:
            empty = True
    return empty


#######################################################################################################
########### DPLL ITSELF ###############################################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()

def dpll_alg(cnf):
    # empty cnf is defined to be valid and therefore satisfiable
    if cnf == []:
        return list()
    # cnf containing empty clauses are by convention unsatisfiable
    elif checkIfEmpty(cnf):
        return "unsat"
    
    # If neither of these cases occour, we start to search the tree for satisfying variable assignments.
    # we do this recursively by repeatedly calling dpll_alg and assigning variables through conditioning
    # until one of the first two cases applies and the cnf is therefore either sat or unsat.
    else:
        # we first select the variable for conditioning 
        var_candidate = findMostCommonVar(cnf)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cnf = conditioning(cnf,var_candidate)

        if dpll_alg(new_cnf) != "unsat":
            var.append(var_candidate)
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            new_cnf_neg = conditioning(cnf,-var_candidate)
            if dpll_alg(new_cnf_neg) != "unsat":
                var.append(-var_candidate)
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                return "unsat"

# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output(cnf):
    output = dpll_alg(cnf)
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

