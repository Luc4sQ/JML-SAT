import numpy as np

# the source is the solve GRASP - so PGRASP

IMPLICATION_GRAPH = list()
CNF = 0
VALUE_ASSIGNMENT = list()
DECISION_ASSIGNMENT = list()

def cdcl(cnf):
    # setting the the global variable
    CNF = cnf
    variableSize = 0
    for i in range(variableSize)
        IMPLICATION_GRAPH.append(list())
        DECISION_ASSIGNMENT.append(False)
        VALUE_ASSIGNMENT.append(False)

    backtracker = 0

    if not search(0,backtracker):
        return False
    else:
        return True

def search(d, beta):

    if decide(d):
        return True
    
    while True:
        if deduce(d):
            if search(d+1, beta)
                return True
            elif beta != d:
                erase()
                return False
        if not diagnose(d, beta):
            erase()
            return False
        
def deduce(d):
    while thereIsUnit() or isUnsatisfied():
        if isUnsatisfied():
            IMPLICATION_GRAPH.append(["k",]) # something !!!
            return False
        if thereIsUnit():
            IMPLICATION_GRAPH.append() # something!!!
            DECISION_ASSIGNMENT[literal] = d
            if literal < 0:
                VALUE_ASSIGNMENT[literal] = 0
            else:
                VALUE_ASSIGNMENT[literal] = 1

    return True

def decide(d):
    chosenVariable, assignedValue = greedyEvaluation()
    IMPLICATION_GRAPH[chosenVariable].append(True)
    VALUE_ASSIGNMENT[chosenVariable] = assignedValue
    DECISION_ASSIGNMENT[chosenVariable] = d

    if isSatisfied():
        return True
    else:
        return False

def greedyEvaluation():
    reducedCNF = list()
    # FIRST: reduce the clause, so the greedy algorithm dont takes clauses, which
    # are already satisfied anyway
    for clause in CNF:
        counter = 0
        for literal in clause:
            if VALUE_ASSIGNMENT[abs(literal)] == 1 and literal > 0:
                continue
            elif VALUE_ASSIGNMENT[abs(literal)] == 0 and literal < 0:
                continue
            else:
                counter += 1
        if counter == len(clause):
            reducedCNF.append(clause)
    
    currentChoice = 0
    currentValue = 0
    maxSum = 0

    # SECOND: summation over all satisfied clauses and record those assignments,
    # which yield a higher sum than before

    for index in range(len(VALUE_ASSIGNMENT)):
        if not VALUE_ASSIGNMENT[index]:
            # case 1: TRUE
            setValue = 1
            sum = 0

            for clause in reducedCNF:
                for literal in clause:
                    if literal > 0 and abs(literal) == index:
                        sum += 1
                        continue
                    elif literal < 0 and abs(literal) == index:
                        continue

            if sum > maxSum:
                currentChoice = index
                currentValue = setValue
                maxSum = sum

            # case 2: FAlSE
            setValue = 0
            sum = 0

            for clause in reducedCNF:
                for literal in clause:
                    if literal < 0 and abs(literal) == index:
                        sum += 1
                        continue
                    elif literal > 0 and abs(literal) == index:
                        continue

            if sum > maxSum:
                currentChoice = index
                currentValue = setValue
                maxSum = sum

    return (currentChoice,currentValue)        


def erase():
    pass