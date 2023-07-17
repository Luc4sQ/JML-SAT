import numpy as np
import src.timing.measure as ms
import src.alg.dpll as dp
from sys import exit

# the source is the solve GRASP - so PGRASP

# global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER

IMPLICATION_GRAPH = list() # adjacency list - stores predecessor

CNF = 0 # stores cnf in numpy form (clause database)
VARIABLEPLACES = list() # stores for each variable, where it belongs in the clause database

REDUCEDCNF = 0 # stores a conditioned form of the cnf
VALUE_ASSIGNMENT = list() # stores value
DECISION_ASSIGNMENT = list() # stores Decision level for each variable
DECISION_TRACKER = list() # stores variables, that were decided or implied in depth d


NUMBEROFVARIABLES = 0
NUMBEROFINITIALCLAUSES = 0
BACKTRACKCOUNTER = 0
ZEROINDICATOR = 0
RANDOMINDEX = 0

def evaluateCNF():
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER

    testCNF = REDUCEDCNF.copy()
    holdAssignment = VALUE_ASSIGNMENT.copy()

    REDUCEDCNF = CNF.copy()

    for depthlist in DECISION_TRACKER:
        for variable in depthlist:
            conditionCNF(variable*VALUE_ASSIGNMENT[variable], True)

    for i, clause in enumerate(REDUCEDCNF):
        if (not isinstance(clause, np.ndarray) or not isinstance(testCNF[i], np.ndarray)) and ( isinstance(clause, np.ndarray) or  isinstance(testCNF[i], np.ndarray)):
            test2cnf = REDUCEDCNF.copy()
            REDUCEDCNF = testCNF.copy()
            VALUE_ASSIGNMENT = holdAssignment.copy()

            return (False, test2cnf)

        if isinstance(clause, np.ndarray) and isinstance(testCNF[i], np.ndarray) and not set(clause) ==  set(testCNF[i]):
            test2cnf = REDUCEDCNF.copy()
            REDUCEDCNF = testCNF.copy()
            VALUE_ASSIGNMENT = holdAssignment.copy()

            return (False, test2cnf)
    
    test2cnf = REDUCEDCNF.copy()
    REDUCEDCNF = testCNF.copy()
    VALUE_ASSIGNMENT = holdAssignment.copy()
        
    return (True, test2cnf)

# takes a clause and a specified literal
# if the clause (without the literal) is satisfied by our assignment it returns True
def isClauseSatisfied(clause, specLiteral = "undefined"):
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    for literal in clause:
        if abs(literal) != specLiteral and literal < 0 and  VALUE_ASSIGNMENT[abs(literal)] == -1:
            return True
        elif abs(literal) != specLiteral and literal > 0 and VALUE_ASSIGNMENT[abs(literal)] == 1:
            return True
    return False

# takes a literal and a boolean indicator "getRemoved"
# True -> normal conditioning operation
# False -> restores clause with literal assumption
def conditionCNF(literal, getRemoved): # variable = welche variabel, getRemoved = bool if it should get removed
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER


    if getRemoved:
        for entries in VARIABLEPLACES[abs(literal)]:
            if (entries[1]*literal) > 0 and  isinstance(REDUCEDCNF[entries[0]], np.ndarray):
                REDUCEDCNF[entries[0]] ="deleted"
            elif (entries[1]*literal) < 0 and isinstance(REDUCEDCNF[entries[0]], np.ndarray):
                npList = REDUCEDCNF[entries[0]]
                REDUCEDCNF[entries[0]] = np.delete(npList,np.argwhere(REDUCEDCNF[entries[0]]==-literal))


        if literal > 0:
            VALUE_ASSIGNMENT[abs(literal)] = 1
        else:
            VALUE_ASSIGNMENT[abs(literal)] = -1


    else:
        # now we want to add a removed variable back again
        for entries in VARIABLEPLACES[abs(literal)]:
            # if the clause previously was deleted cuz it was satisfied
            if not isinstance(REDUCEDCNF[entries[0]], np.ndarray):
                if (VALUE_ASSIGNMENT[abs(entries[1])]*entries[1]) > 0 and not isClauseSatisfied(CNF[entries[0]], abs(entries[1])):
                    clausecopy = CNF[entries[0]].copy()
                    indexes = list()
                    for i, lit in enumerate(clausecopy):
                        if VALUE_ASSIGNMENT[abs(lit)]*lit >= 0:
                            indexes.append(i)
                            
                    REDUCEDCNF[entries[0]] = CNF[entries[0]][indexes].copy()
            else:
                REDUCEDCNF[entries[0]] = np.append(REDUCEDCNF[entries[0]],entries[1])


        VALUE_ASSIGNMENT[abs(literal)] = 0
        IMPLICATION_GRAPH[abs(literal)] = set()

# erases the information in depth d
def erase(d):
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    if len(DECISION_TRACKER) == d+1:
        #print(DECISION_TRACKER[-1])
        for variables in DECISION_TRACKER[d]:
            conditionCNF(variables, False)
        DECISION_TRACKER.pop()
        #print("ERASED Number ",d," so ",DECISION_TRACKER)

# ---------------------------------------------------------------------------------

def greedyEvaluation():
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    currentChoice = 0
    currentValue = 0
    maxSum = 0


    for index in range(len(VALUE_ASSIGNMENT)):
        if index != 0 and VALUE_ASSIGNMENT[index] == 0:

            setValue = 1
            sum = 0

            for clause in REDUCEDCNF:
                if isinstance(clause, np.ndarray):
                    for literal in clause:
                        if literal > 0 and abs(literal) == index:
                            sum += 1
                            continue
                        elif literal < 0 and abs(literal) == index:
                            continue

            if sum >= maxSum:
                currentChoice = index 
                currentValue = setValue
                maxSum = sum

            # case 2: FAlSE
            setValue = -1
            sum = 0

            for clause in REDUCEDCNF:
                if isinstance(clause, np.ndarray):
                    for literal in clause:
                        if literal < 0 and abs(literal) == index:
                            sum += 1
                            continue
                        elif literal > 0 and abs(literal) == index:
                            continue

            if sum >= maxSum:
                currentChoice = index 
                currentValue = setValue
                maxSum = sum

    return (currentChoice,currentValue)    

def easifyReducedCNF():
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    newcnf = REDUCEDCNF.copy()
    index = 0
    while len(newcnf) != index:
        if not isinstance(newcnf[index],np.ndarray):
            del newcnf[index]
        else:
            index += 1
    
    return newcnf



def isSatisfied():
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    for clause in REDUCEDCNF:
        if isinstance(clause, np.ndarray):
            return False
    return True

def decide(d):
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    
    
    #for i, values in enumerate(VALUE_ASSIGNMENT):
    #    if i != 0:
    #        if values == 0:
    #            chosenVariable = i
    #            assignedValue = 1
    
    newcnf = easifyReducedCNF()
    if len(newcnf) == 0:
        return True

    try: 
        chosenVariable = dp.findMostCommonVar(newcnf)
        #print(chosenVariable)
    except:
        #print(CNF)
        #print(REDUCEDCNF)
        #print(REDUCEDCNF)
        for i, values in enumerate(VALUE_ASSIGNMENT):
            if i != 0:
                if values == 0:
                    chosenVariable = i
                    assignedValue = 1


    #print(chosenVariable)
    if chosenVariable > 0:
        assignedValue = 1
    else:
        assignedValue = -1
    
    chosenVariable = abs(int(chosenVariable))
    #chosenVariable, assignedValue = greedyEvaluation()
    VALUE_ASSIGNMENT[chosenVariable] = assignedValue
    if len(DECISION_TRACKER) != d:
        DECISION_TRACKER.append([])
    DECISION_TRACKER.append([chosenVariable])
    DECISION_ASSIGNMENT[chosenVariable] = d
    #print(chosenVariable," : ",assignedValue, " : ",d, "  DECIDED")
    conditionCNF(chosenVariable*assignedValue, True)
    
    
    #print("DECIDED: ",chosenVariable*assignedValue)

    if isSatisfied():
        return True
    else:
        return False

# ---------------------------------------------------------------------------------

def cdcl(cnnf, properties):

    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    NUMBEROFVARIABLES = properties[2]
    NUMBEROFINITIALCLAUSES = properties[3]
    CNF = cnnf.copy()
    REDUCEDCNF = cnnf.copy()

    for i in range(NUMBEROFVARIABLES + 1):
        IMPLICATION_GRAPH.append(set())
        VARIABLEPLACES.append(list())
        VALUE_ASSIGNMENT.append(0)
        DECISION_ASSIGNMENT.append(-1)

    for i, clause in enumerate(cnnf):
        for literal in clause:
            VARIABLEPLACES[abs(literal)].append([i,literal])


    if not search(0):
        return False
    else:
        return True

def search(d):

    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER, RANDOMINDEX
    
    #same, realform = evaluateCNF()
    #
    #if not same:
    #    exit()

    decideTime, decideOutput = ms.timeInSeconds(decide,d)
    if decideOutput:
        return True
    
    
    while True:
        deduceTime, deduceOutput = ms.timeInSeconds(deduce,d)
        #print(d)

        if deduceOutput:
            if search(d+1):
                return True
            elif BACKTRACKCOUNTER != d:
                erase(d)
                return False
        
        diagnoseTime, diagnoseOutput = ms.timeInSeconds(diagnose,d)
        if not diagnoseOutput:
            erase(d)
            #print("gone")
            return False
        
        
        #print("depth<we: ",d, "but its long ",len(DECISION_TRACKER)-1)
        erase(d)
        #print()
        #print("Times:")
        #print("DEDUCE: ", deduceTime)
        print("DECIDE: ",d, " ",len(CNF),end="\r")#" ",REDUCEDCNF[-1], decideTime,"             ",deduceTime,"                   ",diagnoseTime, "   ",end="\r")
        #print(CNF)
        #if len(CNF[-100]) == 1:
        #    exit()
        #print("depth<we: ",d, "but its long ",len(DECISION_TRACKER)-1)
        #if len(REDUCEDCNF[-1]) == 1 and REDUCEDCNF[-1][0] == 67:
           #RANDOMINDEX += 1
            #print(RANDOMINDEX)
        if RANDOMINDEX > 5:
            #print(REDUCEDCNF)
            #print(CNF)
            for  i, clause in enumerate(REDUCEDCNF):
                if len(clause) == 1:
                    pass
                    print(clause)
                    print(CNF[i])
                    print(DECISION_TRACKER)
            exit()
        #print(VALUE_ASSIGNMENT[67])
        #if VALUE_ASSIGNMENT[80] == -1 and len(DECISION_TRACKER) > 4:
        #    exit() 
        #print(REDUCEDCNF)
        #print("DIAGNOSE: ", diagnoseTime)

#----------------------------------------------------------------------------------

def analyseGraph():
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    Graph = IMPLICATION_GRAPH.copy()

    indexVector = set([0])
    newClause = set()

    while len(indexVector) != 0:
        
        listy = set()

        for previousNode in indexVector:
            if len(Graph[previousNode]) == 0:
                newClause.add(-1*previousNode*VALUE_ASSIGNMENT[previousNode])
                continue
            
            listy = listy | Graph[previousNode]

            for node in Graph[previousNode]:
                if previousNode != 0 and DECISION_ASSIGNMENT[previousNode] != DECISION_ASSIGNMENT[node]:
                    newClause.add(-1*node*VALUE_ASSIGNMENT[node])

        indexVector = listy

    
    #print(IMPLICATION_GRAPH[0])
    IMPLICATION_GRAPH[0] = set()

    return np.array(list(newClause))

def diagnose(d):
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER, ZEROINDICATOR
    if len(IMPLICATION_GRAPH[0]) != 0:

        newClause = analyseGraph()
        for literal in newClause:
            VARIABLEPLACES[abs(literal)].append([len(CNF),literal])

        #for clause in CNF:
        #    if not np.array_equal(clause,newClause):
        CNF.append(newClause)

        #print(newClause)
        #print(np.array(VALUE_ASSIGNMENT)[abs(newClause)])
        #print(np.array(DECISION_ASSIGNMENT)[abs(newClause)])
        #print(DECISION_TRACKER)
        BACKTRACKCOUNTER = DECISION_ASSIGNMENT[abs(newClause[0])]

        for literal in newClause:
            if BACKTRACKCOUNTER < DECISION_ASSIGNMENT[abs(literal)]:
                BACKTRACKCOUNTER = DECISION_ASSIGNMENT[abs(literal)]
        #print("BAGGY: ",BACKTRACKCOUNTER, " but ",d)
        if d == 0:
            ZEROINDICATOR += 1
        if ZEROINDICATOR > 1:
            BACKTRACKCOUNTER = -1

        REDUCEDCNF.append(np.array([], dtype=int))

        #print(REDUCEDCNF)

        #if np.array_equal(REDUCEDCNF[0], np.array([], dtype=int)):
        #    print(REDUCEDCNF)
        #    exit()

        DECISION_ASSIGNMENT[0] = -1
        if BACKTRACKCOUNTER != d:
        #    for literal in newClause:
        #        IMPLICATION_GRAPH[0].add(abs(literal))
                
        #    DECISION_ASSIGNMENT[0] = d - 1
            return False
        
        #if len(newClause) == 1:
        #    exit()

        return True
    
    return True
    
#-----------------------------------------------------------------------------------

def thereIsUnit():
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    
    for i, clause in reversed(list(enumerate(REDUCEDCNF))):
        if len(clause) == 1:
            return (clause[0],i)
    return False

def isUnsatisfied():
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER
    for i, clause in enumerate(REDUCEDCNF):
        if len(clause) == 0:
            #print(i)
            return i+1
    return False

def deduce(d):
    global IMPLICATION_GRAPH, CNF, VARIABLEPLACES, REDUCEDCNF, VALUE_ASSIGNMENT, DECISION_ASSIGNMENT, DECISION_TRACKER, NUMBEROFVARIABLES, NUMBEROFINITIALCLAUSES, BACKTRACKCOUNTER, ZEROINDICATOR
    unit = thereIsUnit()
    satis = isUnsatisfied()
    #print("deph: ",d," but decisiontracker ",len(DECISION_TRACKER))
    while unit or satis:

        if satis:
            satis -= 1
            for literal in CNF[satis]:
                IMPLICATION_GRAPH[0].add(abs(literal)) # something !!!

            DECISION_ASSIGNMENT[0] = d
            return False
        if unit:
            literal, clauseIndex = unit
            conditionCNF(literal, True)
            #print("DEDUCED: ",literal)
            for lit in CNF[clauseIndex]:
                
                if abs(lit) != abs(literal):
                    IMPLICATION_GRAPH[abs(literal)].add(abs(lit)) # something!!!
            
            if len(DECISION_TRACKER) == d + 1:
                DECISION_TRACKER[-1].append(abs(literal))
            else:
                DECISION_TRACKER.append([abs(literal)])
                
            DECISION_ASSIGNMENT[abs(literal)] = d


            if literal < 0:
                VALUE_ASSIGNMENT[abs(literal)] = -1
            else:
                VALUE_ASSIGNMENT[abs(literal)] = 1
            #print(abs(literal)," : ",VALUE_ASSIGNMENT[abs(literal)], " : ",d)


        unit = thereIsUnit()
        satis = isUnsatisfied()

    return True