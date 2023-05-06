import time

# this function measures the time a function needs to do its stuff and even returns the functions return values

def timeNeededInSeconds(func, arg):

    start = time.perf_counter()

    try:
        returnValue = func(arg)
    except:
        return (0,0)

    end = time.perf_counter()

    timeSpended = end - start

    return (timeSpended, returnValue)