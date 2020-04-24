from Solver import Solver

solver = Solver('min', v=True)
solver.add_cost([1, 0, 1, 0])  # min: x1 + x3
solver.add_eq_constraint([1, 2, 0, 1, -5])  # x1 + 2x2 +     + x4 = -5
solver.add_eq_constraint([0, 1, 2, 0, 6])   #    +  x2 + 2x3      =  6
solver.solve()
