from Tableau import Tableau
import numpy as np
import matplotlib.pyplot as plt
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

        self.__negeqA = []
        self.__negb = []
        self.__poseqA = []
        self.__posb = []
        self.__eqA = []
        self.__eqb = []

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

    # a1x1 + a2x2 + ... + anxn = bi ---standard---> a1x1 + a2x2 + ... + anxn = bi
    def add_eq_constraint(self, const_term):  # [a1, a2, ..., an, bi]
        self.__eqA.append(const_term[:-1])
        self.__eqb.append(const_term[-1])

    def solve(self):
        # Create an instance of Tableau and iterate for solving that
        # from __negeqA, __poseqA, __eqA to Tableau instance
        self.var = np.arange(len(self.c))

        self.A = np.array(self.__negeqA, dtype=float)
        m = self.A.shape[0]
        n = self.A.shape[1] if len(self.A) > 0 else 0

        self.A = np.c_[self.A, np.eye(m)]

        temp_pos_A = np.array(self.__poseqA, dtype=float)
        m_pos_A = temp_pos_A.shape[0]
        temp = np.c_[temp_pos_A, np.zeros((m_pos_A, m))]
        temp = np.c_[temp, -1*np.eye(m_pos_A)]

        self.A = np.c_[self.A, np.zeros((self.A.shape[0], m_pos_A))]
        if len(temp) > 0:
            self.A = np.vstack((self.A, temp)) if len(self.A) > 0 else temp

        temp_eq_A = np.array(self.__eqA, dtype=float)
        if len(self.__eqA) > 0:  # there is/are equation/s
            n = self.A.shape[1] if len(self.A) > 0 else 0
            m = temp_eq_A.shape[0]
            temp = np.c_[temp_eq_A, np.zeros((m, n))]
            self.A = np.vstack((self.A, temp)) if len(self.A) > 0 else temp

        self.c = np.append(self.c, np.zeros(self.A.shape[1]-len(self.c)))
        self.b = np.append(np.append(self.__negb, self.__posb), self.__eqb)

        # instantiating Tableau
        self._t = Tableau(self.c, self.A, self.b, self.var, self.rule, self.B, self.v, approximation=self.approximation)

        # solving problems
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

        print(f"{bcolors.OKGREEN}{bcolors.BOLD}{bcolors.UNDERLINE}Solution X = "
              f"{var_val}{bcolors.ENDC}")

        sol = round(self._t._z, 4)
        if self.__problem == 'max':
            print("** Max Problem **")
            print(f" z = {sol}")
        else:
            print("** Min Problem **")
            print(f" z = {-1*sol}")

    def plot(self):
        if len(self.var) == 2:
            # plot the feasible region
            d = np.linspace(-2, 16, 300)
            x, y = np.meshgrid(d, d)

            plt.imshow((np.dot(self.__negeqA[0], [x, y]) >= 2).astype(int), extent=(x.min(), x.max(), y.min(), y.max()),
                       origin="lower", cmap="Greys", alpha=0.3)
            plt.show()
            """
            plt.imshow(((y >= 2) & (2 * y <= 25 - x) & (4 * y >= 2 * x - 8) & (y <= 2 * x - 5)).astype(int),
                       extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="Greys", alpha=0.3)
            """
