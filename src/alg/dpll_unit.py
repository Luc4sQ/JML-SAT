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
################################### SEARCH HEURISTICS #################################################
#######################################################################################################

def RAND(cnf):
    knf_variables_list = np.unique(np.concatenate(cnf))
    var = np.random.choice(knf_variables_list)
    return var

def MOMS(cnf):
    
    k = 2
    
    # version with both positive and negative
    #knf_variables_list = np.unique(np.concatenate(cnf))
    
    # version with only positive
    knf_variables_list = np.unique(np.abs(np.concatenate(cnf)))
    
    #print("literals:",knf_variables_list)
            
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
    #print("scores:",scoreArray)
    
    #varWithMaxScore = knf_variables_list[scoreArray==max(scoreArray)]
    varWithMaxScore = np.random.choice(knf_variables_list[scoreArray==max(scoreArray)])
    
    return varWithMaxScore


def JWOS(cnf):
    
    knf_variables_list = np.unique(np.concatenate(cnf))
    
    #print("literals:",knf_variables_list)
    
    scoreArray = np.array([])
    
    for literal in knf_variables_list:
        score = 0
        for clause in cnf:
            if literal in clause:
                score = score + 2**(-len(clause))
                
        scoreArray = np.append(scoreArray,score)
    
    #print("literals:",knf_variables_list)
    #print("scores:",scoreArray)
    varWithMaxScore = np.random.choice(knf_variables_list[scoreArray==max(scoreArray)])
    #varWithMaxScore = knf_variables_list[scoreArray==max(scoreArray)]
    
    return varWithMaxScore

def JWTS(cnf):
    
    knf_variables_list = np.unique(np.concatenate(cnf))
    
    #print("literals:",knf_variables_list)
    
    scoreArray = np.array([])
    
    for literal in knf_variables_list:
        """
        score = 0
        for clause in cnf:
            if literal in clause:
                score = score + 2**(-len(clause))
                
        scoreNeg = 0
        for clause in cnf:
            if -literal in clause:
                scoreNeg = scoreNeg + 2**(-len(clause))
        """
        score = 0
        scoreNeg = 0
        for clause in cnf:
            if literal in clause:
                score = score + 2**(-len(clause))
            if -literal in clause:
                scoreNeg = scoreNeg + 2**(-len(clause))
                
        scoreArray = np.append(scoreArray,score+scoreNeg)
    
    #print("vars:",knf_variables_list)
    #print("scores:",scoreArray)
    #varWithMaxScore = knf_variables_list[scoreArray==max(scoreArray)]
    varWithMaxScore = np.random.choice(knf_variables_list[scoreArray==max(scoreArray)])
    
    return varWithMaxScore


def DLCS(cnf):
    
    cnf_variables_counts = np.unique(np.concatenate(cnf),return_counts=True)
    #print(cnf_variables_counts)
    
    newVars = np.array([])
    newCounts = np.array([])
    
    for var in cnf_variables_counts[0]:
        #print(var)
        if -var not in cnf_variables_counts[0]:
            
            newVars = np.append(newVars,var)
            newCounts = np.append(newCounts,cnf_variables_counts[1][np.where(cnf_variables_counts[0]==var)])
            #print("new vars",newVars,"counts",newCounts)
        else:
            if -var in newVars:
                pass
            else:
                newVars = np.append(newVars,var)
                newCounts = np.append(newCounts,cnf_variables_counts[1][np.where(cnf_variables_counts[0]==var)]+cnf_variables_counts[1][np.where(cnf_variables_counts[0]==-var)])
                #print("new vars",newVars,"counts",newCounts)
    #print("new vars",newVars,"counts",newCounts)
    #litCand = np.select(newCounts==np.max(newCounts),newVars).item()
    litCand = np.random.choice(newVars[newCounts==np.max(newCounts)])
    if -litCand not in cnf_variables_counts[0]:
        lit = litCand
    elif cnf_variables_counts[1][np.where(cnf_variables_counts[0]==litCand)] > cnf_variables_counts[1][np.where(cnf_variables_counts[0]==-litCand)]:
        lit = litCand
    else:
        lit = -litCand
                                                                            
    return(lit)

def DLIS(cnf):
    
    cnf_variables_counts = np.unique(np.concatenate(cnf),return_counts=True)
    
    #var = np.select(cnf_variables_counts[1]==np.max(cnf_variables_counts[1]),cnf_variables_counts[0]).item()
    var = np.random.choice(cnf_variables_counts[0][cnf_variables_counts[1]==np.max(cnf_variables_counts[1])])
    
    #print(cnf_variables_counts[1],cnf_variables_counts[0])
    
    return(var)


#######################################################################################################
########### DPLL ITSELF ADJUSTED WITH UNIT RESOLUTION #################################################
#######################################################################################################

# we initialize an empty list of literals that will be filled with variable assignments in dpll 
var = list()

def dpll_alg_with_unit(cnf,heuristics):
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
            var_candidate = dpll.findMostCommonVar(new_cnf)

        #var_candidate = dpll.findMostCommonVar(new_cnf)

        # then, we recursively search the different "layers" of the tree.
        # for that, the 
        # first for the conditioning on the non-negated variable:
        new_cond_cnf = dpll.conditioning(new_cnf,var_candidate)

        # we need returned dpll literals, so we define them
        dpllOutput = dpll_alg_with_unit(new_cond_cnf,heuristics)

        if dpllOutput != "unsat":
            # building the union over the literals
            var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
            print(var)
            return(var)
        
        # if no satisfiable variable assignment can be found for the non-negated literal, try the negation
        else:
            new_cond_cnf_neg = dpll.conditioning(new_cnf,-var_candidate)
            dpllOutput = dpll_alg_with_unit(new_cond_cnf_neg,heuristics)

            if dpllOutput != "unsat":
                var = list(set([var_candidate]) | set(dpllOutput) | set(resolutedLiterals))
                return(var)
            
        # if no assignment can be found for the negation either, then the cnf is unsat
            else:
                return "unsat"

# generate an output consisting of both a truth value representing satisfiability and a variable assignment that satisfies the cnf if it exists
def output(cnf,heuristics="DLIS"):
    output = dpll_alg_with_unit(cnf,heuristics)
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

