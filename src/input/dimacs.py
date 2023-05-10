import numpy as np
# module for reading a dimacs file

def FileReader(path):

    # exception handler - very short one
    if path == "" or path.split(".")[-1] != "cnf" :
        print("please retry, with a proper file")
        return 0
    else:
        try:
            dimacsFile = open(path)
        except:
            print("Error: no file found. retry with the correct relative path and check the file!")
            return 0

    # two variables for the handling of possible data we need later
    numberOfClauses = 0
    numberOfVariables = 0

    # THE return variable
    KNF = list()

    isFormatConsistent = False

    for line in dimacsFile:
        
        Clause = []

        # ignore the commenting lines in the file
        if line[0] == "c":
            # ... Nothing
            pass

        # a p-line catch
        elif line[0] == "p":

            #converting lines, for iteration and better readability
            convertedLine = line.strip().split(" ")

            numberOfVariables = convertedLine[2]
            numberOfClauses = convertedLine[3]

            if convertedLine[1] == "cnf":
                isFormatConsistent = True

        # case for filtering empty lines. thanks cambridge college
        elif len(line.strip().split(" ")) == 1:
            continue

        else:

            convertedLine = line.strip().split(" ")

            # case for invalid data - weird, will change maybe later
            if not isFormatConsistent:
                print("Error: the data in the file, doesn't have the right format.")
                return 0

            # data hustling for the KNF set
            for data in convertedLine:
                if data != "" and data != "0" and (data.isnumeric() or data[0] == "-"):
                    Clause.append(int(data))

            ClauseSet = np.array(Clause)       

            KNF.append(ClauseSet)

    dimacsFile.close()

    return KNF

                



    

