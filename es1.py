from Solver import Solver

solver = Solver('max', v=True)
solver.add_cost([2, 1])  # max: 2x1 + x2
solver.add_negeq_constraint([1, 0, 2])  # x1       <= 2
solver.add_negeq_constraint([1, 1, 3])  # x1 + x2  <= 3
solver.add_negeq_constraint([1, 2, 5])  # x1 + 2x2 <= 5
solver.solve()
