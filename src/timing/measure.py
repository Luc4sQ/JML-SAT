import time

# this function measures the time a function needs to do its stuff and even returns the functions return values

def timeInSeconds(func, arg):

    start = time.perf_counter()
    
    try:
        if type(arg).__name__ == "tuple":
            returnValue = func(*arg)
        else:
            returnValue = func(arg)
    except:
        print("TimeError. measure.py throws some exception")
        return (0,0)

    end = time.perf_counter()

    timeSpended = end - start

    return (timeSpended, returnValue)