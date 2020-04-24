from Solver import Solver

solver = Solver('min', v=True)
solver.add_cost([1, 1, 10])  # min: x1 + x2 + 10x3
solver.add_eq_constraint([0, 1, 4, 2])    #     + x2 + 4x3 = 8
solver.add_eq_constraint([2, -1, 6, -2])  # 2x1 - x2 + 6x3 = 1
solver.solve()