#!/opt/conda/bin/python3

import argparse
import re
import copy
import itertools

# parser = argparse.ArgumentParser()
# parser.add_argument("-i","--input", help="Input Datei", type=str, required=True)
# args = parser.parse_args()

def brute_force(klauseln):
    
    #Anzahl Variablen bestimmen
    num_var = max(unique([abs(L) for klausel in klauseln for L in klausel]))
    
    #Entscheide die Reihenfolge in der die Belegungen getestet werden
    pos = 0
    neg = 0
    for klausel in klauseln:
        if 1 in klausel:
            pos += 1
        elif -1 in klausel:
            neg += 1       

    #Belegungen generieren
    if neg >= pos:
        belegungen = list(itertools.product([0, 1], repeat=num_var))
    else:
        belegungen = list(itertools.product([1, 0], repeat=num_var))

    #Belegungen testen
    for belegung in belegungen:
        if check(klauseln, belegung):
            return belegung
    return []

def check(klauseln, belegung):
    #teste ob die Belegung alle Klauseln erfüllt 
    for klausel in klauseln:
        if not check_klausel(klausel, belegung):
            return False
    return True

def check_klausel(klausel, belegung):
    #teste ob die Belegung die Klausel erfüllt
    for L in klausel:
        if L > 0:
            if belegung[L-1] == 1:
                return True
        else:
            if belegung[-L-1] == 0:
                return True
    return False

def unique(liste):
    unique_liste = []
    for x in liste:
        if x not in unique_liste:
            unique_liste.append(x)
    return unique_liste



# #Testen
# datei = open(args.input,"r")
# klauseln = []
# for z in datei:
#     if re.search(r" 0$", z):
#         klausel = [int(s) for s in z.split()]
#         if 0 in klausel:
#             klausel.remove(0)
#         klauseln.append(klausel)
#     if re.search(r" %", z):
#         break

# #Zeit stoppen
# import time
# start = time.time()
# erf= brute_force(klauseln)
# end = time.time()
# print("Zeit:",end - start)
# print(erf)