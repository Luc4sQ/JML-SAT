# SAT-Solver für das Logik und KI Seminar

Zusammen programmieren wir hier eine Software, welche die Erfüllbarkeit von aussagenlogischen Formeln entscheidet und gegebenenfalls eine zulässige Belegung angibt

Unser Programm besitzt 3 große verschiedene Algorithmen und viele Möglichkeiten der Auswertung von Daten und erstellung von Datensätzen.

# Installation:

Um unser Programm zu installieren und es zu nutzen, reicht es aus das Repository zu klonen.

```
git clone "https://github.com/Luc4sQ/JML-SAT"
```


# Nutzung:

Unser Programm wird **hauptsächlich** über die Kommandozeile bedient. Man öffnet eine Konsole

- Linux: Terminal
- Windows: Powershell
- MacOS: Bash

und navigiert in den Pfad, in welchem man das GIT Repository geklont hat. Anschließend startet man aufrufe der Form

```
python main.py [argument] [argument2]
```

### Parameter

Über Parameter können verschiedene Funktionen aufgerufen werden. Neben verschiedenen Algorithmen zur Bestimmung der Erfüllbarkeit gibt es auch die Möglichkeit, CNFs zu generieren oder Benchmark Tests auf verschiedenen Files oder Ordnern von Files zu erzeugen. Diese Argumente sind hierunter ausführlich erklärt.

# Algorithmen

Argumente in diesem Block erfolgen nach dem Muster

```
python main.py [argument] [PathToCnfFile]
```

- `-bf` : brute force
- `-dp` : klassisches DP 
- `-dpll` : klassisches DPLL 
- `-cdcl` : GRASP (ein CDCL Algorithmus)
- `-dpll_visual` : visualisierung von DPLL, erzeugt beim Ausführen über die Komandozeile einen Baum und eine .txt Datei (auf der Selben Ebene auf der die CNF Datei, die untersucht wurde, sich befindet), in der mit R eine schöne Visualisierung des vollständigen Suchraums erzeugt werden kann
- `-udpll` : DPLL mit Einheitsresolution
- `-udpll_visual` : Visualisierung von DPLL mit Einheitsresolution analog zu `-dpllple_visual`
- `-dpllple` : DPLL mit Pure-Literal-Elimination
- `-udpll_visual` : Visualisierung von DPLL mit Pure-Literal-Elimination analog zu `-dpllple_visual`
- `-udpllple` : DPLL mit Pure-Literal-Elimination und Einheitsresolution

# Generieren von CNFs
- `-generateCNF` : erlaubt es, aufgrund von Konfigurationen in Form von CNV Dateien Benchmark CNFs zu erstellen. Wenn das Programm mit diesem Parameter aufgerufen wird, muss der Pfad zu der Config Datei gegeben werden. 

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

# Tests über mehrere Files oder Filter mit selbst erstellten Files

Argumente in diesem Block erfolgen nach dem Muster

```
python main.py [argument] [PathToDirectoryOnlyWithCnfFiles]
```

- `-DPLLcomp` : Braucht den Pfad zu einem Ordner mit CNFs, erstellt eine .txt Datei mit Informationen über die durschnittliche Zeit und die Standardabweichung, die die verschiednene Versionen von DPLL (und CDCL) benötigen, um die Erfüllbarkeit zu bestimmen
- `-DPLLcomp_multi` : Alternative zu `DPLLcomp` mit implementiertem Multicorerendering
- `-uDPLLcomp_multi` : Alternative zu `-DPLLcomp_multi` ohne DPLL und DPLL mit Pure-Literal-Elimination
- `-HEURcomp` : Analog zu `-DPLLcomp`, nur dass hier die verschiedenen Heuristiken für DPLL verglichen werden
- `-multiDPLLcomp` : Braucht einen Pfad zu einem Ordner mit Ordnern mit CNFs, die durch dieses Programm erzeugt wurden. Das ist wichtig, weil dadurch Informationen extrahiert werden können, die in der Ausgabe im Vergleichs-csv geschrieben werden. Für jeden dieser Ordner wird `-HEURcomp` aufgerufen und am ende wird im Überordner eine csv Datei erstellt, die die Ergebnisse zusammenfasst.
- `-multiHEURcomp` : Analog zu `-multiDPLLcomp`, nur dass hier die Heuristiken verglichen werden. Die DPLL Variante die hier verwendet wird ist uDPLL.
- `-multiHEURcomp_dpll` : Analog zu `-multiHEURcomp`, nur dass hier DPLL statt uDPLL verwendet wird.

# Komandozeilenbeispiel

Zuallerst wechseln wir das Verzeichnis, sodass wir die `main.py` ausführen können

```
cd JML-SAT/
```

Nun wollen wir eine Datei auf Erfüllbarkeit prüfen mit CDCL

```
python main.py -cdcl ../datasets/50variables/uf50-0501.cnf
```

und erhalten als Ausgabe den Ausdruck

```
True in 0.06377 Sekunden! 
The following variable assignment satisfies input cnf:  not implemented yet
```

Woraus wir ableiten, dass die Formel in `uf50-0501.cnf` erfüllbar ist (Rückgabe: `True`) und die Belegung von diesem Algorithmus noch nicht ausgegeben wird. Alternativ probieren wir DPLL.

```
python main.py -dpll ../datasets/50variables/uf50-0501.cnf
```

und wir erhalten

```
True in 105.88089 Sekunden! 
The following variable assignment satisfies input cnf: {43: False, 22: True, 23: True, 44: True, 46: False, 27: True, 32: False, 42: False, 31: False, 18: False, 7: False, 25: True, 14: True, 48: False, 20: False, 6: True, 13: True, 17: False, 16: False, 39: True, 38: False, 28: True, 33: True, 2: True, 34: True, 12: True, 37: True, 4: True, 15: False, 49: False, 10: True, 1: True, 3: True, 19: True, 36: False, 8: False, 5: True, 50: True, 9: False, 26: True, 47: True, 29: True, 40: False, 30: True, 35: True, 41: False, 45: False, 11: True}
```

sowohl eine Ausgabe (die länger dauerte), als auch eine Belegung.

# Quellen

Die Ressourcen, wo die Algorithmen nachzulesen sind:

- DP: https://resources.mpi-inf.mpg.de/departments/rg1/conferences/vtsa08/slides/barret1_sat.pdf
- DPLL: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh, Handbook of Satisfiability,  ISBN 978-1-58603-929-5
- CDCL: J. P. Marques-Silva and K. A. Sakallah. GRASP: A new search algorithm
for satisfiability. In International Conference on Computer-
Aided Design, Seiten 220–227,