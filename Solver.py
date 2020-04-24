from Tableau import Tableau
import numpy as np
from rules import dantzig_rule
from errors import NoBase, bcolors


# problem = 'min'|'max'
class Solver:
    def __init__(self, problem='max', rule=dantzig_rule, v=False, approximation=8):
        self.v = v
        self.approximation = approximation
        self.c = None
        self.A = None
        self.b = None
        self.B = None
        self.var = None
        self.rule = rule
        self._t = None

        self.__poseqA = []
        self.__posb = []
        self.__negeqA = []
        self.__negb = []

        if problem.lower() not in ['max', 'min']:
            raise AttributeError("problem must be max or min")
        self.__problem = problem.lower()

    def add_cost(self, c):
        self.c = np.array(c, dtype=float) if self.__problem == 'min' else -1*np.array(c, dtype=float)

        # a1x1 + a2x2 + ... + anxn <= bi ---standard---> a1x1 + a2x2 + ... + anxn + si = bi
    def add_negeq_constraint(self, const_term):  # [a1, a2, ..., an, bi]
        self.__negeqA.append(const_term[:-1])
        self.__negb.append(const_term[-1])

    # a1x1 + a2x2 + ... + anxn >= bi ---standard---> a1x1 + a2x2 + ... + anxn - si = bi
    def add_poseq_constraint(self, const_term):  # [a1, a2, ..., an, bi]
        self.__poseqA.append(const_term[:-1])
        self.__posb.append(const_term[-1])

    def solve(self):
        # Create an instance of Tableau and iterate for solving that
        self.var = np.arange(len(self.c))

        self.A = np.array(self.__negeqA, dtype=float)
        m = self.A.shape[0]
        n = self.A.shape[1]
        self.A = np.c_[self.A, np.eye(m)]

        temp_pos_A = np.array(self.__poseqA, dtype=float)
        m = temp_pos_A.shape[0]
        temp = np.c_[temp_pos_A, np.zeros((m, n))]
        temp = np.c_[temp, -1*np.eye(m)]

        self.A = np.c_[self.A, np.zeros((self.A.shape[0], m))]
        self.A = np.vstack((self.A, temp))
        self.c = np.append(self.c, np.zeros(self.A.shape[1]-len(self.c)))
        self.b = np.append(self.__negb, self.__posb)

        self._t = Tableau(self.c, self.A, self.b, self.var, self.rule, self.B, self.v, approximation=self.approximation)

        try:
            while not self._t.isend():
                self._t.step()
                print(self._t)
                print("|| --- --- --- --- --- ||")

            print("|| --- --- --- --- --- --- --- --- --- --- END --- --- --- --- --- --- --- --- --- ||\n")

            self.print_sol()
        except NoBase:
            print("Error in finding a Base")

    def print_sol(self):
        var_val = np.round(self._t.history[-1][0], 4)

        print(f"{bcolors.OKGREEN}{bcolors.BOLD}{bcolors.UNDERLINE}Soluzione [x1, x2] = "
              f"[{var_val[0]}, {var_val[1]}]{bcolors.ENDC}")

        sol = round(self._t._z, 4)
        if self.__problem == 'max':
            print("** Max Problem **")
            print(f" z = {sol}")
        else:
            print("** Min Problem **")
            print(f" z = {-1*sol}")


solver = Solver('max', v=True)
solver.add_cost([-1, 3])
solver.add_negeq_constraint([1, 0, 3])  # <=
solver.add_negeq_constraint([0, 1, 3])  # <=
solver.add_poseq_constraint([4, 3, 12])  # >=
solver.solve()
