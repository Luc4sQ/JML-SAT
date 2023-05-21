import numpy as np
import src.alg.dpll as dpll
import src.alg.dpll_unit as udpll

def getClause(KNF, list, data):
    # Graph initialization
    vertices = list(range(1,data[2]+1))
    edges = list()
    for resolutions in list:
        for literal in KNF[resolutions[1]]:
            if literal != KNF[resolutions[0]]
                edges.append((literal,KNF[resolutions[0]]))

    # calculating conflicts
    conflicts = list()

    

    return

def conditionedFormula(KNF, decisions):
    conditionedKNF = KNF
    for assignment in decisions:
        conditionedKNF = dpll.conditioning(conditionedKNF,assignment)
    
    return conditionedKNF

def expandedUnitResolution(cnf,list):
    # returning of the unitresolution doesnt do anything
    if not cnf:
        return (cnf,list)
    
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

def dpll_plus(KNF, data):

    # numberOfVariables = data[2]
    # numberOfClauses = data[3]
    decisions = list()
    conflicts = list()

    while True:

        unitpropOutput, newList = expandedUnitResolution(list(set(conditionedFormula(KNF)) | set(conflicts)),[])

        if np.array([]) in unitpropOutput:
            if len(decisions) == 0:
                return "unsat"
            else:
                getClause(KNF, newList, data)
                alpha = 

        else:
            if unitpropOutput != []:
                literal = unitpropOutput[0][0]
                assignment = literal
                decisions.append(assignment)
            else:
                return "sat"