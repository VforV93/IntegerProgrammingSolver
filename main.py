
import numpy as np
from errors import DimensionError, NoBase, bcolors
from Tableau import Tableau


def dantzig_rule(c):
    return np.argmin(c)



print("\n|| --- --- --- --- --- --- --- --- --- --- START --- --- --- --- --- --- --- --- --- --- ||")
# n
c = np.array([1, -3, 0, 0, 0], dtype=float)
# m x n
A = np.array([[1, 0, 1, 0, 0],
              [0, 1, 0, 1, 0],
              [4, 3, 0, 0, -1]], dtype=float)
# m
b = np.array([3, 3, 12], dtype=float)

t = Tableau(c, A, b, dantzig_rule)  # , [2,3,4,5])


print("---------")
print(t)
# exit(0)
try:
    while not t.isend():
        t.step()
        print(t)
        print("|| --- --- --- ||")

    var = [0, 1]
    var_val = np.zeros(len(var), dtype=float)
    for i in var:
        if i in t.B:
            var_val[i] = np.dot(t.A[:, i], t.b)

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}{bcolors.UNDERLINE}Soluzione [x1, x2] = [{var_val[0]}, {var_val[1]}]{bcolors.ENDC}")

except NoBase:
    print("Error in finding a Base")
"""
"""