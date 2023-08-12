import numpy as np

# contains dpll along with all the different variations

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
    return var

# since it can't simply be checked, weather an empty array is in a list (empty arrays are assigned a truth value by default), this function checks it
def checkIfEmpty(cnf):
    empty = False
    for element in cnf:
        if len(element)==0:
            empty = True
    return empty


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
                new_cnf = conditioning(cnf,disjunction)
                new_list = list
                new_list.append(float(disjunction))
                new_cnf, new_list = unitResolution(new_cnf,new_list)
                return (new_cnf,new_list)
            
    return (cnf,list)


#######################################################################################################
########### FUNCTIONS USED IN DPLL WITH PURE LITERAL ELIMINATION ######################################
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
                newLitList.append(literal)
                oldCnf = newCnf
                newCnf = list()
                for clause in oldCnf:
                    if literal not in clause:
                        newCnf.append(clause)

        # if something was changed, run pure literal elimination again
        if newCnf != cnf:
            newCnf,newLitList = pureLiteralElimination(newCnf,newLitList)
                        
    return (newCnf,newLitList)


#######################################################################################################
################################### SEARCH HEURISTICS #################################################
#######################################################################################################

def RAND(cnf):
    # create a list of all the literals to choose from based on the cnf
    knf_variables_list = np.unique(np.concatenate(cnf))
    var = np.random.choice(knf_variables_list)
    return var


def MOMS(cnf):
    # choosees variables that occour most often in clauses of minimal size
    
    k = 2
    
    # version with both positive and negative
    #knf_variables_list = np.unique(np.concatenate(cnf))
    
    # version with only positive
    # create a list of all the literals to choose from based on the cnf
    knf_variables_list = np.unique(np.abs(np.concatenate(cnf)))
            
    # find the shortest literal
    shortClauses = np.array([[]])
    for clause in cnf:
        # if the array is empty, add first clause
        if shortClauses[0].size == 0:
            shortClauses = np.array([clause])
        # if shortest clause found so far has same length as considered clause, add considered clause to list
        elif shortClauses[0].size == len(clause):
            shortClauses = np.append(shortClauses,[clause],0)
        # if considered clause is shorter, delete other clauses from list
        elif shortClauses[0].size > len(clause):
            shortClauses = np.array([clause])
    
    scoreArray = np.array([])

    # calculate the score for every variable
    for literal in knf_variables_list:
        occrrenceLiteral = 0
        for clause in shortClauses:
            if literal in clause:
                occrrenceLiteral = occrrenceLiteral +1
        occrrenceNegLiteral = 0
        for clause in shortClauses:
            if -literal in clause:
                occrrenceNegLiteral = occrrenceNegLiteral +1
        score = (occrrenceLiteral + occrrenceNegLiteral)*(2**k) + (occrrenceLiteral*occrrenceNegLiteral)
        scoreArray = np.append(scoreArray,score)

    varWithMaxScore = np.random.choice(knf_variables_list[scoreArray==max(scoreArray)])
    
    return varWithMaxScore


def JWOS(cnf):
    # chooses literal that occours most often in short clauses
    
    # create a list of all the literals to choose from based on the cnf
    knf_variables_list = np.unique(np.concatenate(cnf))
    
    scoreArray = np.array([])
    
    # calculate the score for every literal
    for literal in knf_variables_list:
        score = 0
        for clause in cnf:
            if literal in clause:
                score = score + 2**(-len(clause))
                
        scoreArray = np.append(scoreArray,score)
    
    # amongst the variables with the maximum score, we randomly choose one
    varWithMaxScore = np.random.choice(knf_variables_list[scoreArray==max(scoreArray)])
    
    return varWithMaxScore

def JWTS(cnf):
    # chooses variable that occours most often in short clauses
    
    # create a list of all the literals to choose from based on the cnf
    knf_variables_list = np.unique(np.concatenate(cnf))
    
    scoreArray = np.array([])
    
    # calculate the score for all the literals
    for literal in knf_variables_list:

        score = 0
        scoreNeg = 0
        for clause in cnf:
            if literal in clause:
                score = score + 2**(-len(clause))
            if -literal in clause:
                scoreNeg = scoreNeg + 2**(-len(clause))
                
        scoreArray = np.append(scoreArray,score+scoreNeg)
    
    varWithMaxScore = np.random.choice(knf_variables_list[scoreArray==max(scoreArray)])
    
    return varWithMaxScore


def DLCS(cnf):
    # chooses the variable that occours most often and negates it if negation is more common
    
    # create a list of all the literals to choose from based on the cnf
    cnf_variables_counts = np.unique(np.concatenate(cnf),return_counts=True)
    
    newVars = np.array([])
    newCounts = np.array([])
    
    for var in cnf_variables_counts[0]:
        if -var not in cnf_variables_counts[0]:
            
            newVars = np.append(newVars,var)
            newCounts = np.append(newCounts,cnf_variables_counts[1][np.where(cnf_variables_counts[0]==var)])
        else:
            if -var in newVars:
                pass
            else:
                newVars = np.append(newVars,var)
                newCounts = np.append(newCounts,cnf_variables_counts[1][np.where(cnf_variables_counts[0]==var)]+cnf_variables_counts[1][np.where(cnf_variables_counts[0]==-var)])

    litCand = np.random.choice(newVars[newCounts==np.max(newCounts)])
    if -litCand not in cnf_variables_counts[0]:
        lit = litCand
    elif cnf_variables_counts[1][np.where(cnf_variables_counts[0]==litCand)] > cnf_variables_counts[1][np.where(cnf_variables_counts[0]==-litCand)]:
        lit = litCand
    else:
        lit = -litCand
                                                                            
    return(lit)


def DLIS(cnf):
    # just chooses the most common literal

    # create a list of all the literals to choose from based on the cnf including info about how often they occoured
    cnf_variables_counts = np.unique(np.concatenate(cnf),return_counts=True)
    
    # choose the one that occoured most often
    var = np.random.choice(cnf_variables_counts[0][cnf_variables_counts[1]==np.max(cnf_variables_counts[1])])
    
    return(var)


#######################################################################################################
########### DPLL ITSELF ###############################################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()

def dpll_alg(cnf,heuristics):
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
        if heuristics == "RAND":
            var_candidate = RAND(cnf)
        elif heuristics == "MOMS":
            var_candidate = MOMS(cnf)
        elif heuristics == "JWOS":
            var_candidate = JWOS(cnf)
        elif heuristics == "JWTS":
            var_candidate = JWTS(cnf)
        elif heuristics == "DLIS":
            var_candidate = DLIS(cnf)
        elif heuristics == "DLCS":
            var_candidate = DLCS(cnf)
        else:
            print("ERROR: the heuristics specified are not a valid argument, choosing most common variable instead")
            var_candidate = DLIS(cnf)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cnf = conditioning(cnf,var_candidate)

        if dpll_alg(new_cnf,heuristics) != "unsat":
            var.append(var_candidate)
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            new_cnf_neg = conditioning(cnf,-var_candidate)
            if dpll_alg(new_cnf_neg,heuristics) != "unsat":
                var.append(-var_candidate)
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                return "unsat"

# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output_dpll(cnf,heuristics="DLIS"):
    output = dpll_alg(cnf,heuristics)
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
                variableAssignment.update({int(abs(variable)): False})
    return (satisfiability, variableAssignment)


#######################################################################################################
########### DPLL ITSELF ADJUSTED WITH UNIT RESOLUTION #################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()

def udpll_alg(cnf,heuristics):
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
        if heuristics == "RAND":
            var_candidate = RAND(new_cnf)
        elif heuristics == "MOMS":
            var_candidate = MOMS(new_cnf)
        elif heuristics == "JWOS":
            var_candidate = JWOS(new_cnf)
        elif heuristics == "JWTS":
            var_candidate = JWTS(new_cnf)
        elif heuristics == "DLIS":
            var_candidate = DLIS(new_cnf)
        elif heuristics == "DLCS":
            var_candidate = DLCS(new_cnf)
        else:
            print("ERROR: the heuristics specified are not a valid argument, choosing most common variable instead")
            var_candidate = DLIS(new_cnf)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cond_cnf = conditioning(new_cnf,var_candidate)

        # we need returned dpll literals, so we define them
        dpllOutput = udpll_alg(new_cond_cnf,heuristics)

        if dpllOutput != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            new_cond_cnf_neg = conditioning(new_cnf,-var_candidate)
            dpllOutput = udpll_alg(new_cond_cnf_neg,heuristics)

            if dpllOutput != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                return "unsat"

# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output_udpll(cnf,heuristics="DLIS"):
    output = udpll_alg(cnf,heuristics)
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


#######################################################################################################
########### DPLL WITH PRE LITERAL ELIMINATION #########################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()

def dpllple_alg(cnf,heuristics):

    # applying unit resolution first
    new_cnf, resolutedLiterals = pureLiteralElimination(cnf,[])

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
        if heuristics == "RAND":
            var_candidate = RAND(cnf)
        elif heuristics == "MOMS":
            var_candidate = MOMS(cnf)
        elif heuristics == "JWOS":
            var_candidate = JWOS(cnf)
        elif heuristics == "JWTS":
            var_candidate = JWTS(cnf)
        elif heuristics == "DLIS":
            var_candidate = DLIS(cnf)
        elif heuristics == "DLCS":
            var_candidate = DLCS(cnf)
        else:
            print("ERROR: the heuristics specified are not a valid argument, choosing most common variable instead")
            var_candidate = DLIS(cnf)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cond_cnf = conditioning(new_cnf,var_candidate)

        # we need returned dpll literals, so we define them
        dpllOutput = dpllple_alg(new_cond_cnf,heuristics)

        if dpllOutput != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            new_cond_cnf_neg = conditioning(new_cnf,-var_candidate)
            dpllOutput = dpllple_alg(new_cond_cnf_neg,heuristics)

            if dpllOutput != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                return "unsat"

# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output_dpllple(cnf,heuristics="DLIS"):
    output = dpllple_alg(cnf,heuristics)
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


#######################################################################################################
########### DPLL WITH UNIT RESOLUTION AND PRE LITERAL ELIMINATION #####################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()

def udpllple_alg(cnf,heuristics):

    # applying unit resolution first
    new_cnf, resolutedLiterals = unitResolution(cnf,[])
    new_cnf, resolutedLiterals = pureLiteralElimination(new_cnf, resolutedLiterals)

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
        if heuristics == "RAND":
            var_candidate = RAND(cnf)
        elif heuristics == "MOMS":
            var_candidate = MOMS(cnf)
        elif heuristics == "JWOS":
            var_candidate = JWOS(cnf)
        elif heuristics == "JWTS":
            var_candidate = JWTS(cnf)
        elif heuristics == "DLIS":
            var_candidate = DLIS(cnf)
        elif heuristics == "DLCS":
            var_candidate = DLCS(cnf)
        else:
            print("ERROR: the heuristics specified are not a valid argument, choosing most common variable instead")
            var_candidate = DLIS(cnf)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cond_cnf = conditioning(new_cnf,var_candidate)

        # we need returned dpll literals, so we define them
        dpllOutput = udpllple_alg(new_cond_cnf,heuristics)

        if dpllOutput != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            new_cond_cnf_neg = conditioning(new_cnf,-var_candidate)
            dpllOutput = udpllple_alg(new_cond_cnf_neg,heuristics)

            if dpllOutput != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                return "unsat"

# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output_udpllple(cnf,heuristics="DLIS"):
    output = udpllple_alg(cnf,heuristics)
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