# module for reading a dimacs file

def FileReader(path):

    # exception handler - very short one
    if path == "" or path.split(".")[-1] != "knf" :
        print("please retry, with a proper file")
        return 0
    else:
        dimacsFile = open(path)
    
    # two variables for the handling of possible data we need later
    numberOfClauses = 0
    numberOfVariables = 0

    # THE return variable
    KNF = {}

    for line in dimacsFile:

        Clause = {}
        
        # ignore the commenting lines in the file
        if line[0] == "c":
            # ... Nothing
            pass

        else:
            #converting lines, for iteration and better readability
            convertedLine = line.split(" ")
            linePrefix = convertedLine[0]

            # a p-line catch
            if not linePrefix.isnumeric():
                numberOfVariables = convertedLine[2]
                numberOfClauses = convertedLine[3]

            # data hustling for the KNF set
            else:
                for data in convertedLine:
                    if data.isnumeric():
                        Clause.add(data)

        KNF.add(Clause)

    dimacsFile.close()

    return KNF

                



    

