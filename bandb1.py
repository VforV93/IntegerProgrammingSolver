

from Solver import Solver
from BeB import BeB


solver = Solver('max', v=True)
solver.add_cost([1, 2])  # max: x1 + 2x2
solver.add_negeq_constraint([4, 6, 24])  # 4x1 + 6x2 <= 24
solver.add_poseq_constraint([2, 1, 4])   # 2x1 +  x2  <= 4
solver.add_negeq_constraint([0, 1, 3])   #     +  x2 <= 3
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
          f"{beb.z}. Max Problem solution cost {-1*beb.z}")
else:
    print("No Integer Solution")
print(beb)