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
    KNF = set()

    isFormatConsistent = False

    for line in dimacsFile:
        
        Clause = []

        # ignore the commenting lines in the file
        if line[0] == "c":
            # ... Nothing
            pass

        else:
            #converting lines, for iteration and better readability
            convertedLine = line.strip().split(" ")

            linePrefix = convertedLine[0]

            # a p-line catch
            if linePrefix == "p":
                numberOfVariables = convertedLine[2]
                numberOfClauses = convertedLine[3]

                if convertedLine[1] == "cnf":
                    isFormatConsistent = True

            # data hustling for the KNF set
            else:

                if not isFormatConsistent:
                    print("Error: the data in the file, doesn't have the right format.")
                    return 0

                for data in convertedLine:
                    if not data == "" and (data.isnumeric() or data[0] == "-"):
                        Clause.append(data)

                ClauseSet = frozenset(Clause)       

                KNF.add(ClauseSet)

    dimacsFile.close()

    return KNF

                



    

