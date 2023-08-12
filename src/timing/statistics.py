import numpy as np
import glob as gl
import src.input.dimacs as sid
import src.timing.measure as ms
import src.alg.bruteforce as br
import src.alg.dpll as dpll
#import src.alg.dpll_unit as udpll
import src.alg.dp as dp
import src.alg.cdcl as cdcl

def reportStatistics(dataVector):
    mean_v = np.mean(dataVector)
    std_v = np.std(dataVector)

    return (mean_v,std_v)

def makeMultipleKNFs(path, arg):
    #print(path + "/*.cnf")
    pathVector = gl.glob(path + "/*")
    print(pathVector)
    timesPerTry = list()

    i = 0
    for paths in pathVector:
        cnf, properties = sid.FileReader(paths)
        print(cnf)
        print(properties)
        print(paths)
        if arg == "-cdcl":
            time, output = ms.timeInSeconds(cdcl.cdcl, (cnf,properties))

        if arg == "-udpll":
            #time, output = ms.timeInSeconds(udpll.output, cnf)

        if arg == "-dpll":
            time, output = ms.timeInSeconds(dpll.output, cnf)

        if arg == "-bf":
            time, output = ms.timeInSeconds(br.bruteForce, (cnf, properties))

        if arg == "-dp":
            time, output = ms.timeInSeconds(dp.backtrack, (cnf, properties))

        timesPerTry.append(time)
        print(i)
        i +=1
    return timesPerTry




