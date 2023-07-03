import numpy as np

# test 

def unitPropagation(cnf, ass):
    pass

def allVariablesAssigned():

    return True

def pickBranchingVariable():

    pass

def conflictAnalysis(cnf, ass):

    pass

def backtrack(cnf, ass, beta):

    pass

def cdcl(cnf, assignment):
    if unitPropagation(cnf,assignment) == "conflict":
        return "unsat"
    dl = 0

    while not allVariablesAssigned():
        x = pickBranchingVariable() # heuristik?

        dl += 1

        assignment = assignment | set(x)

        if unitPropagation(cnf, assignment) == "conflict":
            beta = conflictAnalysis(cnf, assignment)

            if beta < 0:
                return "unsat"
            else:
                backtrack(cnf, assignment, beta)
                dl = beta                
    
    
    pass