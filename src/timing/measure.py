import time

# this function measures the time a function needs to do its stuff and even returns the functions return values

def timeInSeconds(func, arg):
    start = time.perf_counter()
    
    #try:
    if type(arg).__name__ == "tuple":
        returnValue = func(*arg)
    else:
        returnValue = func(arg)
    #except:
    #    print("TimeError. measure.py throws some exception")
    #    return (0,0)

    end = time.perf_counter()

    timeSpended = end - start

    return (timeSpended, returnValue)

# for comparing heuristics we need to also include information about which heuristic we want to try
def timeInSecondsHeuristics(func, arg, heuristics):

    start = time.perf_counter()
    
    try:
        if type(arg).__name__ == "tuple":
            returnValue = func(*arg,heuristics)
        else:
            returnValue = func(arg,heuristics)
    except:
        print("TimeError. measure.py throws some exception")
        return (0,0)

    end = time.perf_counter()

    timeSpended = end - start

    return (timeSpended, returnValue)