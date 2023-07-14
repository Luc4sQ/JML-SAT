import numpy as np

# the source is the solve GRASP - so PGRASP

IMPLICATION_GRAPH = list() # adjacency list - stores predecessor

CNF = 0 # stores cnf in numpy form (clause database)
VARIABLEPLACES = list() # stores for each variable, where it belongs in the clause database

REDUCEDCNF = 0 # stores a conditioned form of the cnf
VALUE_ASSIGNMENT = list() # stores value
DECISION_TRACKER = list() # stores variables, that were decided or implied in depth d

NUMBEROFVARIABLES = 0
NUMBEROFINITIALCLAUSES = 0
BACKTRACKCOUNTER = 0

# takes a clause and a specified literal
# if the clause (without the literal) is satisfied by our assignment it returns True
def isClauseSatisfied(clause, specLiteral = "undefined"):
    for literal in clause:
        if abs(literal) != specLiteral and literal < 0 and VALUE_ASSIGNMENT[abs(literal)] == 0:
            return True
        elif abs(literal) != specLiteral and literal > 0 and VALUE_ASSIGNMENT[abs(literal)] == 1:
            return True
    return False

# takes a literal and a boolean indicator "getRemoved"
# True -> normal conditioning operation
# False -> restores clause with literal assumption
def conditionCNF(literal, getRemoved): # variable = welche variabel, getRemoved = bool if it should get removed
    if getRemoved:
        for entries in VARIABLEPLACES[abs(literal)]:
            if entries[1]*literal > 0 and REDUCEDCNF[entries[0]] != "deleted":
                REDUCEDCNF[entries[0]] ="deleted"
            elif entries[1]*literal < 0 and REDUCEDCNF[entries[0]] != "deleted":
                REDUCEDCNF[entries[0]] = np.delete(REDUCEDCNF[entries[0]],np.argwhere(REDUCEDCNF[entries[0]]==-literal))

        if literal > 0:
            VALUE_ASSIGNMENT[abs(literal)] = 1
        else:
            VALUE_ASSIGNMENT[abs(literal)] = -1


    else:
        # now we want to add a removed variable back again
        for entries in VARIABLEPLACES[abs(literal)]:
            # if the clause previously was deleted cuz it was satisfied
            if REDUCEDCNF[entries[0]] == "deleted":
                if VALUE_ASSIGNMENT[abs(literal)]*entries[1] > 0 and not isClauseSatisfied(REDUCEDCNF[entries[1]], abs(literal)):
                    REDUCEDCNF[entries[0]] = CNF[entries[0]]
            else:
                np.append(REDUCEDCNF[entries[0]],entries[1])


        VALUE_ASSIGNMENT[abs(literal)] = False
        IMPLICATION_GRAPH[abs(literal)] = list()

# erases the information in depth d
def erase(d):

    for variables in DECISION_TRACKER[d]:
        conditionCNF(variables, False)

    DECISION_TRACKER.pop()

# ---------------------------------------------------------------------------------

def greedyEvaluation():
    
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

            for clause in REDUCEDCNF:
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
            setValue = -1
            sum = 0

            for clause in REDUCEDCNF:
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

def isSatisfied():
    for clause in REDUCEDCNF:
        if clause != "deleted":
            return False
    return True

def decide(d):
    chosenVariable, assignedValue = greedyEvaluation()
    VALUE_ASSIGNMENT[chosenVariable] = assignedValue
    DECISION_TRACKER.append(chosenVariable)
    conditionCNF(chosenVariable*assignedValue, True)

    if isSatisfied():
        return True
    else:
        return False

# ---------------------------------------------------------------------------------

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
            if search(d+1):
                return True
            elif BACKTRACKCOUNTER != d:
                erase()
                return False
        if not diagnose(d):
            erase()
            return False

def diagnose():
    pass

def thereIsUnit():
    for clause in REDUCEDCNF:
        if len(clause) == 1:
            return clause[0]
    return False

def isUnsatisfied():
    for i, clause in enumerate(REDUCEDCNF):
        if len(clause) == 0:
            return i
    return False

def deduce(d):
    unit = thereIsUnit()
    satis = isUnsatisfied()

    while unit or satis:

        if satis:
            andecent = list()
            for literal in CNF[satis]:
                IMPLICATION_GRAPH[0].append(literal) # something !!!

            return False
        
        if unit:
            conditionCNF(unit, True)
            
            for literal in CNF
            IMPLICATION_GRAPH[abs(unit)] # something!!!

            DECISION_ASSIGNMENT[literal] = d
            if literal < 0:
                VALUE_ASSIGNMENT[literal] = -1
            else:
                VALUE_ASSIGNMENT[literal] = 1

        unit = thereIsUnit()
        satis = isUnsatisfied()

    return True


    
