
import numpy as np
from Solver import Solver
from errors import NoBase, bcolors
from Tableau import Tableau
from rules import dantzig_rule
from BeB import BeB, depth_first


# Goal: we want to find the best integer solution on usage of ingredients to prepare recipes
# in order to obtain the best benefits in term of (stomach, health, sanity)
#                                                       Recipes
#               | - - -- - - | Meatballs | Waffles | Bacon&Egg | Roasted_Berries | Skewer1 | Skewer2 |
# Ingredients   | Meat       | 1         |         | 2         |                 | 1       | 1       | <= actual value
#               | Butter     |           | 1       |           |                 |         |         | <= actual value
#               | Berries    |           | 1       |           | 1               | 2       |         | <= actual value
#               | Egg        |           | 1       | 1         |                 |         | 1       | <= actual value
#               | Filler     | 3         | 1       | 1         |                 | 1       | 2       | <= actual value
# Objective function max Σw*(st, he, sa)rj where w = (wst, whe, wsa), importance of measurement in % (sum = 1) ex (0.3, 0.5, 0.2)

# Meatballs         = (62.5, 3, 5)
# Waffles           = (37.5, 60, 5)
# Bacon&Egg         = (75, 20, 5)
# Roasted_Berries   = (12.5, 1, 0)
# Skewer1           = (37.5, 3, 10)
# Skewer2           = (37.5, 3, 10)


recipes = ['Meatballs', 'Waffles', 'Bacon&Egg', 'Roasted_Berries', 'Skewer1', 'Skewer2']
recipes_benefit = {'Meatballs': [62.5, 3, 5],
                   'Waffles': [37.5, 60, 5],
                   'Bacon&Egg': [75, 20, 5],
                   'Roasted_Berries': [12.5, 1, 0],
                   'Skewer1': [37.5, 3, 10],
                   'Skewer2': [37.5, 3, 10]}
weights = [.4, .4, .2]

c = np.ndarray(len(recipes), dtype=float)
for i, r in enumerate(recipes):
    c[i] = np.dot(weights, recipes_benefit[r])
print(f"cost vector {c}\n")

solver = Solver('max', rule=dantzig_rule, v=True)
solver.add_cost(c)
solver.add_negeq_constraint([1, 0, 2, 0, 1, 1, 9])
solver.add_negeq_constraint([0, 1, 0, 0, 0, 0, 2])
solver.add_negeq_constraint([0, 1, 0, 1, 2, 0, 13])
solver.add_negeq_constraint([0, 1, 1, 0, 0, 1, 3])
solver.add_negeq_constraint([3, 1, 1, 0, 1, 2, 20])
solver.solve()

solver._t.v = 0  # for the B&B verbosity of Tableau set to 0
# I want the best integer solution
print("\n|| --- --- --- --- --- --- --- --- --- START B&B --- --- --- --- --- --- --- --- --- --- ||")
beb = BeB(solver._t, v=1)
while not beb.isend():
    beb.expand()

print("\nBranch and Bound End!")
if beb.best_int_sol is not None:
    print(f"Best integer solution: {beb.best_int_sol} ===> solution cost: "
          f"{round(beb.z, 2)}. Max Problem solution cost {-1*round(beb.z, 2)}")
else:
    print("No Integer Solution")
print(beb)