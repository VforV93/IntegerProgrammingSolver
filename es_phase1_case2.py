import numpy as np
from errors import DimensionError, NoBase, NoSolution, RankAWrong, bcolors
from Tableau import Tableau

from rules import bland_rule

print("\n|| --- --- --- --- --- --- --- --- --- --- START --- --- --- --- --- --- --- --- --- --- ||")
# n
c = np.array([1, 1, 10], dtype=float)
# m x n
A = np.array([[0, 1, 4],
              [2, -1, 6]], dtype=float)
# m
b = np.array([2, -2], dtype=float)
var = np.array([0, 1, 2], dtype=int)

try:
    t = Tableau(c, A, b, var, bland_rule)
except NoSolution as e:
    print(f"{bcolors.FAIL} {e} {bcolors.ENDC}")
    exit(1)
except RankAWrong as e:
    print(f"{bcolors.FAIL} {e} {bcolors.ENDC}")
    exit(1)

print("---------")
print(t)

try:
    while not t.isend():
        t.step()
        print("|| --- --- --- --- --- ||")

    print("|| --- --- --- --- --- --- --- --- --- --- END --- --- --- --- --- --- --- --- --- ||\n")
    var_val = np.zeros(len(t.var), dtype=float)
    for i in t.var:
        if i in t.B:
            var_val[i] = np.dot(t.A[:, i], t.b)

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}{bcolors.UNDERLINE}Soluzione [x1, x2, x3] = [{var_val[0]}, "
          f"{var_val[1]}, {var_val[2]}]{bcolors.ENDC}")

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