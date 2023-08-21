#!/opt/conda/bin/python3
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-i","--input", help="Input Datei", type=str, required=True)
# args = parser.parse_args()


#dp algorithmus
def dp(klauseln):
    
    #pruefen, ob wir fertig sind
    if len(klauseln) == 0:
        return True

    #check if [] in klauseln
    if [] in klauseln:
        return False

    # 1 literal rule
    for klausel in klauseln:
        if len(klausel)==1:
            L=klausel[0]
            return dp(unit_res(klauseln,L))
    
    #doppelte Klauseln entfernen
    klauseln = unique(klauseln)      
    
    #subsumption rule
    klauseln=subsume_rm(klauseln)     
    
    
    #affirmative negative rule
    pure_literale = []
    unpure_literale = []   
    for klausel in klauseln:
        for L in klausel:
            if -L in pure_literale:
                pure_literale.remove(-L)
                unpure_literale.append(-L)
                unpure_literale.append(L)
            elif (L not in unpure_literale and L not in pure_literale):
                    pure_literale.append(L)

    if len(pure_literale) > 0:
        for L in pure_literale:
            return dp(unit_res(klauseln,L))        
    
    #resolution rule
    zaehler = {}
    for klausel in klauseln:
        for literal in klausel:
            if abs(literal) not in zaehler:
                zaehler[abs(literal)] = {"pos":0, "neg":0}
            if literal > 0:
                zaehler[abs(literal)]["pos"] += 1
            else:
                zaehler[abs(literal)]["neg"] += 1

    L = min(zaehler, key=lambda x: zaehler[x]["pos"] * zaehler[x]["neg"])    

    pos = []
    neg = []
    neutral = []
    for klausel in klauseln:
        if L in klausel:
            klausel.remove(L)
            pos.append(klausel)
        elif -L in klausel:
            klausel.remove(-L)
            neg.append(klausel)
        else:
            neutral.append(klausel)
            
    neu = []
    
    for k1 in pos:
        for k2 in neg:
            k3 = k1 + k2            
            k3 = unique_int(k3)
            loeschen = False
            for l in list(k3):
                if l in k3 and -l in k3:
                    loeschen = True
            if loeschen == False:
                neu.append(k3)
    neu = neu + neutral
    return dp(neu)


#Funktion für unit-res (1 literal rule)
def unit_res(klauseln, literal):
    klauseln_res = [klausel for klausel in klauseln if literal not in klausel]
    klauseln_res = [[x for x in klausel if x != -literal] for klausel in klauseln_res]
    return klauseln_res

def subsume_rm(klauseln):
    klauseln=unique(klauseln)
    l = len(klauseln)
    i= 0
    j= 0
    while i < l:
        while j < l:
            if is_subset(klauseln[i],klauseln[j]) and i<j:
                klauseln.remove(klauseln[j])
                l-=1
            elif is_subset(klauseln[i],klauseln[j]) and i>j:
                klauseln.remove(klauseln[j])
                l-=1
                i-=1
            else:
                j+=1
        i+=1
        j = 0
                
    return klauseln


def is_subset(klausel1,klausel2):
    if len(klausel1)<len(klausel2):
        if len(unique([klausel2,unique_int(klausel1+klausel2)]))==1:
            return True    
    return False

def unique_int(liste):
    unique_liste = []
    for i in liste:
        if i not in unique_liste:
            unique_liste.append(i)
    return unique_liste

def unique(liste):
    unique_liste = [liste[0]]
    for x in liste:
        duplicate = False
        for y in unique_liste:
            if len(x)==len(y):
                i = 0
                for l1 in x:
                    if l1 not in y:
                        i+=1
                if i == 0:
                    duplicate = True
        if not duplicate:
            unique_liste.append(x)
    return unique_liste

# #Testen
# import re

# datei = open(args.input, "r")
# klauseln = []
# for z in datei:
#     if re.search(r" 0$", z):
#         klausel = [int(s) for s in z.split()]
#         if 0 in klausel:
#             klausel.remove(0)
#         klauseln.append(klausel)
#     if re.search(r" %", z):
#         break

# import time
# start = time.time()
# erf= dp(klauseln)
# import time
# ende = time.time()
# print("Zeit:",ende - start)
# print(erf)
