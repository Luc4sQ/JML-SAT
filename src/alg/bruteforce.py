import numpy as np
# brute force method

def bruteForce(KNF, properties):
    # p1 = clause, p2 = variables
    satisfiable = True

    numberOfVariables = properties[1]
    numberOfClauses = properties[0]
    expo = 2**numberOfVariables

    for i in range(0,expo):

        assignment = np.zeros(numberOfVariables)
        bitIndex = i

        print("Progress: ",i, " von ",expo,end = "\r")

        for j in range(0,numberOfVariables):
            if bitIndex%2 == 1:
                assignment[j] = 1
            else:
                assignment[j] = -1
            bitIndex = int(bitIndex/2)

        #print(assignment)

        for k in range(0,numberOfClauses):
            recentClause = KNF[k]
            satisfiableClause = True

            for l in range(0,recentClause.size):
                if recentClause[l] < 0 and assignment[np.abs(recentClause[l])-1] < 0:
                    break
                elif recentClause[l] > 0 and assignment[recentClause[l]-1] > 0:
                    break
                elif l == recentClause.size - 1:
                    satisfiableClause = False

            if not satisfiableClause:
                break

        if not satisfiableClause:
            continue
        else: 
            print("",end = "\n")
            return satisfiable
    
    print("",end = "\n")
    return not satisfiable
