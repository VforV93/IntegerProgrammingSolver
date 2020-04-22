
import numpy as np
from Tableau import Tableau
from rules import bland_rule
from BeB import BeB

# Goal: we want to find the best integer solution on usage of ingredients to prepare recipes
# in order to obtain the best benefits in term of (stomach, health, sanity)
#                                                       Recipes
#               | - - -- - - | Meatballs | Waffles | Bacon&Egg | Roasted_Berries | Skewer1 | Skewer2 |
# Ingredients   | Meat       | 1         |         | 2         |                 | 1       | 1       | <= actual value
#               | Butter     |           | 1       |           |                 |         |         | <= actual value
#               | Berries    |           | 1       |           | 2               | 2       |         | <= actual value
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

print(np.round(c))
c = np.round(c)
A = np.array([[1, 0, 2, 0, 1, 1, 1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 1, 0, 2, 2, 0, 0, 0, 1, 0, 0],
              [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
              [3, 1, 1, 0, 1, 2, 0, 0, 0, 0, 1]], dtype=float)
c_min = np.append(c, np.zeros(A.shape[0]))
c_min = -1 * c_min  # from max --> min
b = np.array([9, 2, 13, 3, 20], dtype=float)
var = np.array([0, 1, 2, 3, 4, 5], dtype=int)


t = Tableau(c_min, A, b, var, rule=bland_rule, v=1)
print("---------")
print(t)

while not t.isend():
    t.step()
    print("|| --- --- --- --- --- ||")

t.v = 0  # for the B&B verbosity of Tableau set to 0
# I want the best integer solution
print("\n|| --- --- --- --- --- --- --- --- --- START B&B --- --- --- --- --- --- --- --- --- --- ||")
beb = BeB(t, v=1)
while not beb.isend():
    beb.expand()

print("\nBranch and Bound End!")
if beb.best_int_sol is not None:
    print(f"Best integer solution: {beb.best_int_sol} ===> solution cost: "
          f"{-1*np.dot(beb.best_int_sol, c)}. Max Problem costo solution {np.dot(beb.best_int_sol, c)}")
else:
    print("No Integer Solution")