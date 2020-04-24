from Solver import Solver

solver = Solver('max', v=True)
solver.add_cost([-1, 3])  # max: -x1 + 3x2
solver.add_negeq_constraint([1, 0, 3])   # x1        <= 3
solver.add_negeq_constraint([0, 1, 3])   # x1 + x2   <= 3
solver.add_poseq_constraint([4, 3, 12])  # 4x1 + 3x2 <= 12
solver.solve()