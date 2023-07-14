import numpy as np

# the source is the solve GRASP - so PGRASP

IMPLICATION_GRAPH = list() # adjacency list - stores predecessor
CNF = 0 # stores cnf in numpy form (clause database)
REDUCEDCNF = 0 # stores a conditioned form of the cnf
VARIABLEPLACES = list() # stores for each variable, where it belongs in the clause database
VALUE_ASSIGNMENT = list() # stores value
DECISION_TRACKER = list() # stores variables, that were decided or implied in depth d
NUMBEROFVARIABLES = 0
NUMBEROFINITIALCLAUSES = 0
BACKTRACKCOUNTER = 0

def isClauseSatisfied(clause, specLiteral = "undefined"):
    for literal in clause:
        if literal != specLiteral and literal < 0 and VALUE_ASSIGNMENT[abs(literal)] == 0:
            return True
        elif literal != specLiteral and literal > 0 and VALUE_ASSIGNMENT[abs(literal)] == 1:
            return True
    return False

def conditionCNF(literal, getRemoved): # variable = welche variabel, getRemoved = bool if it should get removed
    if getRemoved:
        # conditioning code of melanie related to dpll
        new_cnf = list()
        for entry in REDUCEDCNF:
            #if (len(entry)==0):
            #    new_cnf.append(np.array([]))
            if entry != "deleted" and literal not in entry:
                if -literal in entry:
                    index = np.argwhere(entry==-literal)
                    new_entry = np.delete(entry,index)
                    new_cnf.append(new_entry)
                else:
                    new_cnf.append(entry)
            else:
                new_cnf.append("deleted")  
        REDUCEDCNF = new_cnf

    else:
        # now we want to add a removed variable back again
        for entries in VARIABLEPLACES[abs(literal)]:
            # if the clause previously was deleted cuz it was satisfied
            if REDUCEDCNF[entries[0]] == "deleted":
                if VALUE_ASSIGNMENT[abs(literal)]*entries[1] > 0 and not isClauseSatisfied(REDUCEDCNF[entries[1]]):
                    REDUCEDCNF[entries[0]] = CNF[entries[0]]
            else:
                np.append(REDUCEDCNF[entries[0]],entries[1])


        VALUE_ASSIGNMENT[abs(literal)] = False

def erase(d):




def cdcl(cnf, properties):
    # setting the the global variable
    NUMBEROFVARIABLES = properties[2]
    NUMBEROFINITIALCLAUSES = properties[3]
    CNF = cnf
    REDUCEDCNF = cnf
    for i in range(NUMBEROFVARIABLES + 1):
        IMPLICATION_GRAPH.append(list())
        VARIABLEPLACES.append(list())
        VALUE_ASSIGNMENT.append(False)

    for i, clause in enumerate(cnf):
        for literal in clause:
            VARIABLEPLACES[abs(literal)].append([i,literal])




    if not search(0):
        return False
    else:
        return True

def search(d):

    if decide(d):
        return True
    
    while True:
        if deduce(d):
            if search(d+1)
                return True
            elif BACKTRACKCOUNTER != d:
                erase()
                return False
        if not diagnose(d):
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
                VALUE_ASSIGNMENT[literal] = -1
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
