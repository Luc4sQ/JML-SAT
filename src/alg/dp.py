import numpy as np

#bucket_set
bucket_set = []

#function for ordering the variables
def orderOfVariables(properties):
    order = []
    for var in range(1,properties[2]+1):
        order.append(var)
    return order

#this function takes a clause and insert it in the right bucket
def fillingBucket(clause,order):
    for index in range(len(order)): 
        if ((order[index] in clause) ^ (-order[index] in clause)):
            bucket_set[index].append(np.array(clause))
            return
    return

#unit resolution for variable var
def unitResolution(var, cnf):
    new_cnf = []
    for clause in cnf:
        if -var in clause:
            if len(clause) == 1:
                new_cnf.append([])
                return new_cnf
            else:
                index = np.argwhere(clause == -var)
                new_clause = np.delete(clause,index)
                new_cnf.append(new_clause)

        elif var not in clause and -var not in clause:
            new_cnf.append(clause)

    return new_cnf  

#resolution for two given clauses
def resolution(clause1, clause2):
    resolvent = []
    for var1 in clause1:
        if var1 not in resolvent and -var1 not in clause2:
            resolvent.append(var1)
    for var2 in clause2:
        if var2 not in resolvent and -var2 not in clause1:
            resolvent.append(var2)

    return np.array(resolvent)

#function takes a bucket and the variable of the bucket
#try unit resolution, checks if variable occur only positiv or negativ in a bucket, resolution
#return a set of resolvents
def processingBucket(var, bucket):
    resolvents = []

    #unit resolution 
    #if unit resolution is possible, the bucket is succesfully processed
    for i in range(len(bucket)):
        if len(bucket[i]) == 1:
            resolvents = unitResolution(bucket[i][0], bucket)
            return resolvents
    
    #if unit resolution is not possible: check, if variables occur only positive or only negative
    #creating positiv and negativ list
    pos = []
    neg = []
    
    #filling the lists
    for clause in bucket:
        if var in clause:
            pos.append(clause)
        else:
            neg.append(clause)

    #if one of them is empty, there are no resolvents and the bucket is succesfully processed
    if len(pos)==0 or len(neg)==0:
        return resolvents

    #resolution an var using all pairs of clauses from pos and neg
    for index1 in range(len(pos)):
        for index2 in range(len(neg)):
            resolvent = resolution(pos[index1],neg[index2])
            if len(resolvent) != 0:
                    resolvents.append(resolvent)
    
    return resolvents
            
#checking, if a cnf contains empty clause   
def isEmpty(cnf):
    for element in cnf:
        if len(element)==0:
            return True
    return False



#Algorithm
def dp(cnf, properties):

    if len(cnf) == 0:
        return "sat"
    elif isEmpty(cnf):
        return "unsat"
    else:
        #ordering variables (algorithm for getting a better order?)
        order = orderOfVariables(properties)

        #creating a bucket in bucketset for every variable
        for var in order:
            bucket_set.append([])
        
        #filling the clauses into the buckets
        for clause in cnf:
            fillingBucket(clause,order)
        
        #checking every buckets. If the buckets is not empty, process the bucket
        for index in range(len(order)):
            #print(index+1)
            if len(bucket_set[index]) != 0:
                resolvents = processingBucket(order[index], bucket_set[index])
                if isEmpty(resolvents):
                    return "unsat"
                #insert resolvents from resolution in buckets
                elif len(resolvents) != 0:
                    for clause in resolvents:
                        fillingBucket(clause,order)
        
        return "sat"

def backtrack(cnf, properties):
    alg = dp(cnf, properties)

    if alg == "unsat":
        satisfiable = False
        variableAssignment = {}
    
    else:
        satisfiable = True
        variableAssignment = {}
    
    return(satisfiable, variableAssignment)
