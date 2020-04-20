
import numpy as np
from errors import NoBase, bcolors
from Tableau import Tableau
from rules import bland_rule
from BeB import BeB

print("\n|| --- --- --- --- --- --- --- --- --- --- START --- --- --- --- --- --- --- --- --- --- ||")
# n
c = np.array([-1, -2, 0, 0, 0], dtype=float)
# m x n
A = np.array([[4, 6, 1, 0, 0],
              [2, 1, 0, -1, 0],
              [0, 1, 0, 0, 1]], dtype=float)
# m
b = np.array([24, 4, 3], dtype=float)
var = np.array([0, 1], dtype=int)

t = Tableau(c, A, b, var, bland_rule)  # , [2,3,4,5])


print("---------")
print(t)

try:
    while not t.isend():
        t.step()
        print("|| --- --- --- --- --- ||")

    print("|| --- --- --- --- --- --- --- --- --- --- END --- --- --- --- --- --- --- --- --- ||\n")

    var_val = t.history[-1][0]

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}{bcolors.UNDERLINE}Soluzione [x1, x2] = [{var_val[0]}, {var_val[1]}]{bcolors.ENDC}")
    print("** Min Problem **")
    sol = t._z
    print(f"-z =  {sol}")
    sol = -1 * sol
    print(f" z = {sol}")
    print("** Max Problem **")
    sol = -1 * sol
    print(f" z = {sol}")
except NoBase:
    print("Error in finding a Base")


beb = BeB(t)
while not beb.isend():
    beb.expand()

print("FINE")