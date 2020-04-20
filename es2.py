
import numpy as np
from errors import NoBase, bcolors
from Tableau import Tableau
from rules import dantzig_rule


print("\n|| --- --- --- --- --- --- --- --- --- --- START --- --- --- --- --- --- --- --- --- --- ||")
# n
c = np.array([1, -3, 0, 0, 0], dtype=float)
# m x n
A = np.array([[1, 0, 1, 0, 0],
              [0, 1, 0, 1, 0],
              [4, 3, 0, 0, -1]], dtype=float)
# m
b = np.array([3, 3, 12], dtype=float)
var = np.array([0, 1], dtype=int)

t = Tableau(c, A, b, var, dantzig_rule, v=1)


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