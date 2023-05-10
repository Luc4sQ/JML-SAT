import sys

# module to handle powershell/terminal arguments
def getArguments(argsForAlgorithm):

    # list of arguments
    argumentList = sys.argv
    argumentList.pop(0) # remove "main.py" argument
    numberOfArguments = len(argumentList)

    # this happens, when nonsense or nothing is supplied via arguments
    if numberOfArguments != 2 or not argumentList[0] in (argsForAlgorithm | {"--help"}):
        print("wrong arguments supplied. please type --help for more information")
        return (0,0)
    
    # this prints the help text. 
    if argumentList[0] == "--help":
        print("py main.py [ARG] [PATH] \npy main.py [ARG]\n\nARG: argument which specifies the used algorithm.")
        print("PATH: relative path to a .cnf file\n \nPossible arguments:")
        for args in argsForAlgorithm:
            print("--> "+args)
        return (0,0)

    # information about algorithm argument and returning path/arg
    return (argumentList[0],argumentList[1])