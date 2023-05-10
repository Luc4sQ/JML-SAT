# SAT-Solver für das Logik und KI Seminar

Zusammen programmieren wir hier eine Software, welche die Erfüllbarkeit von aussagenlogischen Formeln entscheidet und gegebenenfalls eine zulässige Belegung angibt

### Auszug aus Main-Prozedur:

Eingebunden werden unsere Module bspw. durch Aufrufe der Form

```
import src.dp as dp
import src.input.args as arg
import src.input.dimacs as sid
```
Anschließend suchen wir den Block, in dem die Hauptprozedur läuft
```
if path != 0:

    KNF = sid.FileReader(path)
    
    if KNF != 0:

        ########## HERE is the main procedure place. ADD CODE HERE ########## 

        if specifiedArgument == "-dp":
            func, satisfiable = dp.DP(exampleset)

        print("out knf is ", satisfiable, "-able")

        #####################################################################
```

### Komandozeilenbeispiel

Angenommen unsere Prozedur heißt "main.py" und es gibt

- "-dp" als Argument für DP
- "-dpll" als Argument für DPLL

dann führen wir unser Programm aus durch

```
py main.py -dp ../testfile.cnf
```

Jedoch besitzt der Aufruf des Programms einen eigenen "Help Handler".

Frage: Variablen (oder längeninformationen) beifügen zum Set?

### Quellen

- Sets: https://www.w3schools.com/python/python_sets.asp
- Tupel: https://www.w3schools.com/python/python_tuples.asp (Ausgabe damit, statt einer Liste?)
- Map als Datenstruktur gibt es wohl nicht als Grundbibliothek, also ein $2 \times V$ Vektor als Alternative? ($V$ = Anzahl der Variablen)