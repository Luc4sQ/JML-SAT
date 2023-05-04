# Importing some stuff
import sys as arg
import src.input.dimacs as sid

# functioning code! returns a serious KNF
KNF = sid.FileReader("../../CBS_k3_n100_m411_b30_13.cnf")

print(KNF)


