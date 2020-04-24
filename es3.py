from Solver import Solver

solver = Solver('max', v=True)
solver.add_cost([1, 2])  # max: x1 + x2
solver.add_negeq_constraint([1, 1, 8])   # x1 + x2 <= 8
solver.add_poseq_constraint([1, -1, 1])  # x1 - x2 >= 1
solver.add_negeq_constraint([1, 0, 6])   # x1      <= 6
solver.solve()