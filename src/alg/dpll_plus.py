import numpy as np
import src.alg.dpll as dpll
import src.alg.dpll_unit as udpll

def conflictAnalysis(KNF, lists, decisions, data):
    # Graph initialization
    vertices = list()
    for i in range(0,data[2]):
        vertices.append(i+1)
    vertices.append("empty")
    edges = list()
    
    for resolutions in lists:
        for literal in KNF[resolutions[1]]:
            if literal != resolutions[0]:
                edges.append((literal,resolutions[0]))

    # calculating conflicts
    conflicts = list()

    sideA = list()
    sideB = list()

    for dec in decisions:
        sideA.append(dec)
        vertices.remove(dec)
    sideB.append("empty")
    vertices.remove("empty")

    for j in range(0, 2**len(vertices)):

        bitIndex = j

        for k in range(0,len(vertices)):
            if bitIndex%2 == 1:
                sideB.append(vertices[k])
            bitIndex = int(bitIndex/2)

        literals = set()

        for edge in edges:
            if edge[1] in sideB and not edge[0] in sideB:
                literals.add(edge[0])

        if len(literals) == 1:
            if literals[0] in decisions:
                assertionLevel = decisions.index(literals[0])
            else:
                assertionLevel = len(decisions)
            return (np.array(list(literals)), assertionLevel)
        
        conflicts.append(np.array(list(literals)))

        # reset
        sideB = ["empty"]

    mainconflict = conflicts[0]
    for clause in conflicts:
        if len(clause) < len(mainconflict):
            mainconflict = clause

    levels = set()

    assertionLevel = len(decisions)

    if len(mainconflict) == 1:
        assertionLevel == -1
    else:
        for thingy in mainconflict:
            if thingy in decisions:
                levels.add(decisions.index(thingy))
            else:
                levels.add(len(decisions))

        if len(levels) == 1:
            assertionLevel = levels[0]
        else:
            levels.remove(max(levels))
            assertionLevel = max(levels)

    return (mainconflict,assertionLevel)

def conditionedFormula(KNF, decisions):
    conditionedKNF = KNF
    for assignment in decisions:
        conditionedKNF = dpll.conditioning(conditionedKNF,assignment)
    
    return conditionedKNF

def expandedUnitResolution(cnf,list):
    # returning of the unitresolution doesnt do anything
    if not cnf:
        return (cnf,list)
    
    # returning in the special case we encounter a contradiction
    elif np.array([]) in cnf:
        index = cnf.index(np.array([]))
        new_list = list
        if len(list) > 0:
            indexshift = index
            for entry in list:
                if entry[1] <= index:
                    indexshift += 1
            new_list.append(["empty",indexshift])
        else:
            new_list.append(["empty",index])

        return (cnf,new_list)


    else:
        for i in range(0,len(cnf)):
            # recursively implementing unit resolution by using conditioning of dpll file
            if len(cnf[i]) == 1:
                new_cnf = dpll.conditioning(cnf,cnf[i])
                new_list = list
                if len(list) > 0:
                    indexshift = i
                    for entry in list:
                        if entry[1] <= i:
                            indexshift += 1
                    new_list.append([float(cnf[i]),indexshift])
                else:
                    new_list.append([float(cnf[i]),i])
                new_cnf, new_list = expandedUnitResolution(new_cnf,new_list)
                return (new_cnf,new_list)
            
    return (cnf,list)

def isInList(array, listOfArrays):
    for arrays in listOfArrays:
        if np.array_equal(array, arrays):
            return True
    
    return False

def dpll_plus(KNF, data):

    decisions = list()
    conflicts = list()

    while True:

        watchedKNF = conditionedFormula(KNF, decisions)

        for conflict in conflicts:
            watchedKNF.append(conflict)

        unitpropOutput, resolutedLiterals = expandedUnitResolution(watchedKNF,[])
        print(np.array([], dtype=np.dtype(np.float64)) == unitpropOutput[0])
        print(np.array_equal(np.array([], dtype=np.dtype(np.float64)),unitpropOutput[0]))
        print(np.array([], dtype=np.dtype(np.float64)) in unitpropOutput)
        print(" decision : ",decisions)
        print(unitpropOutput)

        if isInList(np.array([], dtype=np.dtype(np.float64)), unitpropOutput):
            if len(decisions) == 0:
                return "unsat"
            else:
                # conflict analysis
                conflictClause, m = conflictAnalysis(KNF, resolutedLiterals, decisions, data)
                while len(decisions) >= m:
                    decisions.pop()
                conflicts.append(conflictClause)
        else:
            if unitpropOutput != []:
                decisions.append(unitpropOutput[0][0])
            else:
                return "sat"