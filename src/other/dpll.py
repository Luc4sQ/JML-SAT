#!/opt/conda/bin/python3

import argparse
import re

# parser = argparse.ArgumentParser()
# parser.add_argument("-i","--input", help="Input Datei", type=str, required=True)
# args = parser.parse_args()
         
def dpll(klauseln, belegung):
        
    # Abbruchbedingungen
    if len(klauseln) == 0:
        return True, belegung
    
    for klausel in klauseln:
        if len(klausel) == 0:
            return False, []

    # 1 literal rule    
    for klausel in klauseln:
        if len(klausel)==1:
            L=klausel[0]
            belegung.append(L)
            k_neu=unit_res(klauseln,L)
            return dpll(k_neu,belegung)

    # Variablenwahl Aufteilungsregel
    zaehler = {}
    for klausel in klauseln:
        for literal in klausel:
            if abs(literal) not in zaehler:
                zaehler[abs(literal)] = {"pos":0, "neg":0}
            if literal > 0:
                zaehler[abs(literal)]["pos"] += 1
            else:
                zaehler[abs(literal)]["neg"] += 1
    
    L = max(zaehler, key=lambda x: zaehler[x]["pos"] + zaehler[x]["neg"])
    
    # Entscheidung welcher Backtrackingpfad
    if zaehler[L]["pos"] >= zaehler[L]["neg"]:
        beleg_1 = belegung + [L]
        k_1 = unit_res(klauseln,L)
        beleg_2 = belegung + [-L]
        k_2 = unit_res(klauseln,-L)
    else:
        beleg_1 = belegung + [-L]
        k_1 = unit_res(klauseln,-L)
        beleg_2 = belegung + [L]
        k_2 = unit_res(klauseln,L)

    e1,b1=dpll(k_1,beleg_1)
    if e1:
        return True, b1
    return dpll(k_2,beleg_2)


# Hilfsfunktionen
def unit_res(klauseln, literal):
    klauseln_res = [klausel for klausel in klauseln if literal not in klausel]
    klauseln_res = [[x for x in klausel if x != -literal] for klausel in klauseln_res]
    return klauseln_res


# Testen

## Klauseln einlesen
#datei = open(args.input,"r")
#klauseln = []
#for z in datei:
#    if re.search(r" 0$", z):
#        klausel = [int(s) for s in z.split()]
#        if 0 in klausel:
#            klausel.remove(0)
#        klauseln.append(klausel)
#    if re.search(r" %", z):
#        break
        
# DPLL aufrufen und Zeit stoppen
#import time
#start = time.perf_counter()
#erf,bel= dpll(klauseln,[])
#end = time.perf_counter()
#print("Zeit:",end - start)
#print(erf)
#print("Belegung:",bel)