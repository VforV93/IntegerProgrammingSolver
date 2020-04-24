
import numpy as np
from errors import NoBase, bcolors
from Tableau import Tableau
from rules import dantzig_rule


print("\n|| --- --- --- --- --- --- --- --- --- --- START --- --- --- --- --- --- --- --- --- --- ||")
# n
c = np.array([-3/4, 20, -0.5, 6, 0, 0, 0], dtype=float)
# m x n
A = np.array([[1/4, -8, -1, 9, 1, 0, 0],
              [1/2, -12, -1/2, 3, 0, 1, 0],
              [0, 0, 1, 0, 0, 0, 1]], dtype=float)
# m
b = np.array([0, 0, 1], dtype=float)
var = np.array([0, 1, 2], dtype=int)
B = np.array([4, 5, 6], dtype=int)
t = Tableau(c, A, b, var, dantzig_rule, v=1, z=3)


print("---------")
print(t)

try:
    while not t.isend():
        t.step()
        print(t)
        print("|| --- --- --- --- --- ||")

    print(t)
    print("|| --- --- --- --- --- --- --- --- --- --- END --- --- --- --- --- --- --- --- --- ||\n")

    var_val = np.zeros(len(t.var), dtype=float)
    for i in t.var:
        if i in t.B:
            var_val[i] = np.round(np.dot(t.A[:, i], t.b), 4)

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}{bcolors.UNDERLINE}Solution [x1, x2, x3] = "
          f"[{var_val[0]}, {var_val[1]}, {var_val[2]}]{bcolors.ENDC}")
    print("** Min Problem **")
    sol = round(t._z, 4)
    print(f"-z =  {sol}")
    sol = -1 * sol
    print(f" z = {sol}")
    print("** Max Problem **")
    sol = -1 * sol
    print(f" z = {sol}")
except NoBase:
    print("Error in finding a Base")