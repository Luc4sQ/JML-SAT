import time as t

# this function measures the time a function needs to do its stuff and even returns the functions return values

def timeNeededInSeconds(func, arg):

    start = t.perf_counter()

    try:
        returnValue = func(arg)
    except:
        return (0,0)

    end = t.perf_counter()

    timeSpended = end - start

    return (timeSpended, returnValue)