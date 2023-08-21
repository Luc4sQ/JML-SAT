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

### Parameter

Über Parameter können verschiedene Funktionen aufgerufen werden. Neben verschiedenen Algorithmen zur Bestimmung der Erfüllbarkeit gibt es auch die Möglichkeit, CNFs zu generieren oder Benchmark Tests auf verschiedenen Files oder Ordnern von Files zu erzeugen:

# Algorithmen
- "-bf" : brute force
- "-dp"
- "-dpll" : klassischer DPLL 
- "-dpll_visual" : visualisierung von DPLL, erzeugt beim Ausführen über die Komandozeile einen Baum und eine .txt Datei (auf der Selben Ebene auf der die CNF Datei, die untersucht wurde, sich befindet), in der mit R eine schöne Visualisierung des vollständigen Suchraums erzeugt werden kann
- "-udpll" : DPLL mit Unit Resolution
- "-udpll_visual" : Visualisierung von DPLL mit Unit Resolution analog zu "-dpllple_visual"
- "-dpllple" : DPLL mit Pure Literal Elimination
- "-udpll_visual" : Visualisierung von DPLL mit Pure Literal Elimination analog zu "-dpllple_visual"
- "-udpllple" : DPLL mit Pure Literal Elimination und Unit Resolution

# Generieren von CNFs
- "-generateCNF" : erlaubt es, aufgrund von Konfigurationen in Form von CNV Dateien Benchmark CNFs zu erstellen. Wenn das Programm mit diesem Parameter aufgerufen wird, muss der Pfad zu der Config Datei gegeben werden. 

Die oberste Zeile der Config CSV sollte dabei wie folgt lauten: 
"Number,Vars,ClauseCount,ClauseCountDet,ClauseLen,ClauseLenDet"
Dabei bezeichnen die Namen:
- Number: Anzahl der Formeln, die je für satisfiable und nicht satisfiable generiert werden sollen
- Vars: Anzahl der Variablen
- ClauseCount: Anzahl der Klauseln
- ClauseCountDet: Soll Die Anzahl der Klauseln immer wie angegeben sein (dann "DET") oder aus einer Normalverteilung mit dem angegebenen Wert als Mittelwert gezogen werden (Dann "ND") ?
- ClauseLen: Länge der Klauseln
- ClauseLenDet: Analog zu "ClauseCountDet"

Die gewünschten Charakteristika können dann in dieser Reihenfolge angegeben werden. Eine Beispiel Ziele, die einen Datensatz generieren würde, wäre:
100,20,100,"DET",3,"DET"
Für jede Zeile werden zwei Ordner mit den Dateien erstellt: Einer mit erfüllbaren und einer mit nicht erfüllbaren Formeln.
Es kann sein, dass einer der beiden Ordner leer ist, das liegt daran, dass das Programm bei dem Versuch, sowohl so viele erfüllbare als auch so viele nicht erfüllbare CNFs zu erstellen wie gewünscht, nur maximal zehn mal so viele CNFs generiert und testet wie generiert werden sollen. Sonst würde das Programm bei manchen Parameterkombinationen, bei denen Erfüllbarkeit oder Nicht-Erfüllbarkeit sehr unwahrscheinlich ist, endlos lange laufen.

- "-findVarThreshold" : Testet für gegebene Anzahl an Variablen und Klausellänge den Anteil an erfüllbaren von 400 erzeugten KNFS für verschiedene Klausel-Anzahlen und berechnet die durchschnittliche Berechnungszeit. Gibt eine Graphik aus, die die Ergebnisse veranschaulicht. Parameterwerte können im Code geändert werden.

# Tests über mehrere Files oder Filter mit selbst erstellten Files
- "-DPLLcomp" : Braucht den Pfad zu einem Ordner mit CNFs, erstellt eine .txt Datei mit Informationen über die durschnittliche Zeit und die Standardabweichung, die die verschiednene Versionen von DPLL benötigen, um die Erfüllbarkeit zu bestimmen
- "-HEURcomp" : Analog zu "-DPLLcomp", nur dass hier die verschiedenen Heuristiken für DPLL verglichen werden
- "-multiDPLLcomp" : Braucht einen Pfad zu einem Ordner mit Ordnern mit CNFs, die durch dieses Programm erzeugt wurden. Das ist wichtig, weil dadurch Informationen extrahiert werden können, die in der Ausgabe im Vergleichs-csv geschrieben werden. Für jeden dieser Ordner wird "-HEURcomp" aufgerufen und am ende wird im Überordner eine csv Datei erstellt, die die Ergebnisse zusammenfasst.
- "-multiHEURcomp" : Analog zu "multiDPLLcomp", nur dass hier die Heuristiken verglichen werden. Die DPLL Variante die hier verwendet wird ist uDPLL.
- "-multiHEURcomp_dpll" : Analog zu "-multiHEURcomp", nur dass hier DPLL statt uDPLL verwendet wird.

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