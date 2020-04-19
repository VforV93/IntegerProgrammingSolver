import numpy as np
from errors import DimensionError, NoBase, NoSolution, RankAWrong, bcolors
from Tableau import Tableau

from rules import bland_rule

print("\n|| --- --- --- --- --- --- --- --- --- --- START --- --- --- --- --- --- --- --- --- --- ||")
# n
c = np.array([1, 0, 1, 0], dtype=float)
# m x n
A = np.array([[1, 2, 0, 1],
              [0, 1, 2, 0]], dtype=float)
# m
b = np.array([-5, 6], dtype=float)
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