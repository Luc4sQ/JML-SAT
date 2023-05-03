# SAT-Solver für das Logik und KI Seminar

Zusammen programmieren wir hier eine Software, welche die Erfüllbarkeit von aussagenlogischen Formeln entscheidet und gegebenenfalls eine zulässige Belegung angibt

### Eingabebeispiel: ("func" ist die map, welche die Belegung darstellt)

```
import "../DP/DP.py" as dp

exampleset = {{1, -2}, {-1, 2}}

func, satisfiable = dp.DP(exampleset)

print("out knf is ", satisfiable, "-able")
```

### Komandozeilenbeispiel

Angenommen unsere Prozedur heißt "main.py" und es gibt

- "-dp" als Argument für DP
- "-dpll" als Argument für DPLL

dann führen wir unser Programm aus durch

```
py main.py -dp testfile.dimacs
```

Frage: Variablen (oder längeninformationen) beifügen zum Set?