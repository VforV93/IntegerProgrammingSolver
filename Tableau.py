import numpy as np
from errors import DimensionError, NoBase, NoSolution, RankAWrong, bcolors
import copy


class Tableau:
    def __init__(self, c, A, b, var, rule, B=None, v=False, approximation=6):
        self.c = c                  # cost vector
        self.A = A                  # constraint matrix coefficients
        self.b = b                  # constant terms vector
        self.var = var              # indexes of the "real" variables
        self.B = np.repeat(-1, self.A.shape[0])
        self.rule = rule            # Function to choose wich column enter to the Base
        self.v = v  # Verbosity
        self.history = list()
        self._z = float(0)          # solution cost
        self.__savesol = False
        self.__appr = approximation

        # Check dimensions length of c, A, and b
        m = self.A.shape[0]  # num of rows
        n = self.A.shape[1]  # num of columns
        if not len(self.c) == n:
            raise DimensionError("Cost vector length must be equal to n(# A Columns)")
        if not len(self.b) == m:
            raise DimensionError("Constant terms length must be equal to m(# A Rows)")

        if self.v:
            print(self)

        if B is not None:
            self.B = np.array(B, dtype=int)
            self.__azzera_costi_base()
            self.save_sol()
        else:
            # applying phase 1
            if not self._base():
                if self.v:
                    print(f"{bcolors.WARNING}No starting Base founded! ==> Phase1{bcolors.ENDC}")
                self.phase1()

        if self.v:
            print(self)
        self.__savesol = True  # after the phase1 I want to store all the pivoting iteration sol and cost

    """
    # Final Tableau if all cost coefficients are positive OR it is not possible to identify a feasible base
    """
    def isend(self):
        if not self._base():
            if self.v:
                print(f"{bcolors.FAIL}Feasible Base does not exist!{bcolors.ENDC}")
            raise NoBase("Feasible Base does not exist!")

        if np.max(self.c[self.B]) != 0 or np.min(self.c[self.B]) != 0:
            self.__azzera_costi_base()
            if self.v:
                print(self)

        if np.min(self.c) < 0:
            return False
        else:
            return True

    def step(self, rule=None):
        if self.v:
            print("Eseguendo Pivoting...")
        #TODO before pivoting I want to save the states to take track of all the steps

        # for pivoting I need a feasible base
        if not self._base():
            print(f"{bcolors.WARNING}Pivoting not possible, a feasible Base does not exist.{bcolors.ENDC}")
            return False

        if np.max(self.c[self.B]) != 0:
            self.__azzera_costi_base()
            print(self)

        if self.isend():
            if self.v:
                print("Stop Pivoting - End!")
            return True
        if not rule:
            rule = self.rule
        j = rule(self.c)
        pivot = self._pivot(j)
        i = pivot[0]
        self.__pivoting(i, j)
        self.B[np.argmax(self.A[:, j])] = j
        # self._base()

        if self.__savesol:
            self.save_sol()

        if self.v:
            print("...Ending Pivoting")
        return self.A

    # individuate the coordinate(i,j) of the pivot corresponding on column j
    def _pivot(self, j):
        i = []
        _min = 1000
        for r in range(0, self.A.shape[0]):
            if self.A[r, j] > 0:
                ba = self.b[r]/self.A[r, j]
                if ba < _min:
                    _min = ba
                    i = [r]
                elif ba == _min:
                    i.append(r)
        if len(i) > 1:  # parity on the choice of the pivot
            for ib in self.B:  # the most left column in base must go out - blend rule specification
                pos_1 = np.argmax(self.A[:, ib])  # 1's position in the ib's column
                if pos_1 in i:
                    return pos_1, j
        return i[0], j

    def __pivoting(self, i, j):
        p = self.A[i, j]
        if self.v:
            print("Pivot founded:{:.3f} in column: {}, row: {}".format(p, j, i + 1))
        # column j enter to the Base and the corresponding one, consequently, exit
        i = i + 1
        A = np.column_stack((self.A, self.b))
        A = np.row_stack((np.append(self.c, self._z), A))
        # pivot row divided by the pivot value
        A[i] = A[i] / p

        # tutte le altre righe le sommo/sottraggo alla riga del pivot stessa
        # moltiplicata per il valore nella colonna del pivotstesso
        # al fine di annullare qualsiasi termine nella colonna del pivot --> colonna ENTRANTE
        for r in range(0, len(A)):
            if r == i or A[r, j] == 0:
                continue
            A[r] = A[r] - A[r, j] * A[i]

        # Status update
        self.c = np.around(A[0, :-1], self.__appr)
        self._z = np.around(A[0, -1], self.__appr)
        self.A = np.around(A[1:, :-1], self.__appr)
        self.b = np.around(A[1:, -1], self.__appr)

    """
    # If exist a Base, found it and return True, False otherwise. Check also that the b's values are non negative
    """
    def _base(self):
        if self.__check_positive_b() and \
           (self.A[:, self.B].shape[0] == self.A[:, self.B].shape[1]) and \
           np.allclose(self.A[:, self.B], np.eye(self.A[:, self.B].shape[0])):
            return True
        else:
            if self.v:
                print("Identifying a Base...")
        # mxm
        m = self.A.shape[0]
        temp_B = np.full(m, -1, dtype=int)
        n = self.A.shape[1]

        # ran = range(0, n)
        for j in range(0, n)[::-1]:
            cnz = np.count_nonzero(self.A[:, j])
            summo = self.A[:, j].sum()
            if summo == 1 and cnz == 1:
                temp_B[np.argmax(self.A[:, j])] = j

        if np.amin(temp_B) >= 0:
            self.B = temp_B
            if self.v:
                print(f"{bcolors.OKGREEN}found Base B: {self.B}{bcolors.ENDC}")
                print(self)
            self.__azzera_costi_base()
            return True
        else:
            if self.v:
                print(f"{bcolors.WARNING}Base not found{bcolors.ENDC}")
            return False

    """
    # constant terms must be non negative
    # return: True if all bs are non negative, False if at least one term is being change to positive(-1 * b)
    """
    def __check_positive_b(self):
        ret = True
        # Check if the b values are positive
        min_el = np.argmin(self.b)
        while self.b[min_el] < 0:
            self.b[min_el] = -1 * self.b[min_el]
            self.A[min_el] = -1 * self.A[min_el]
            min_el = np.argmin(self.b)
            ret = False

        return ret

    def __azzera_costi_base(self):
        if not self._base():
            if self.v:
                print("There's no any Base")
            return False
        if np.amin(self.c[self.B]) == 0 and np.amax(self.c[self.B]) == 0:
            if self.v:
                print("Base cost already zero")
            return True

        for j in self.B:
            if self.c[j] != 0:
                molt = self.c[j]
                self.c = self.c - molt * self.A[np.argmax(self.A[:, j]), :]
                self._z = self._z - molt * self.b[np.argmax(self.A[:, j])]

        if self.v:
            print("Base costs set to zero")
        return True

    # Find a Starting Feasible Solution for the Simplex Algorithm
    def phase1(self):
        if self.v:
            print(f"\n{bcolors.OKGREEN}||=== === === === ===> Starting Phase 1...{bcolors.ENDC}")
        phase_tableau = copy.deepcopy(self)
        phase_tableau.c.fill(0)
        m = self.A.shape[0]  # num of rows
        phase_tableau._z = 0
        phase_tableau._add_variable(np.ones(m, dtype=float), np.eye(m))
        phase_tableau.B = np.array(range(len(phase_tableau.c)-m, len(phase_tableau.c)))
        artificial_base = copy.deepcopy(phase_tableau.B)
        phase_tableau.__azzera_costi_base()

        if self.v:
            print(phase_tableau)
        while not phase_tableau.isend():
            phase_tableau.step()
            if self.v:
                print(phase_tableau)

        # 3 Possibilities:
        # 1) All artificial variables out, True variables in Base
        check = np.isin(phase_tableau.B, artificial_base)

        if not check.any():
            self.A = copy.deepcopy(phase_tableau.A[:, :self.A.shape[1]])
            self.B = copy.deepcopy(phase_tableau.B)
            self.b = copy.deepcopy(phase_tableau.b)
            # self._z = copy.deepcopy(phase_tableau._z)
            if self.v:
                print(f"{bcolors.OKGREEN}||=== === === === ===> Phase 1 Completed!{bcolors.ENDC}\n\n")
            self.__azzera_costi_base()
            self.save_sol()
            return True
        else:  # some artificial variable in Base ==> Fail
            # 3) Original problem no solution
            if phase_tableau.sol > 0:
                print(f"{bcolors.FAIL}||=== === === === ===> Phase 1 Failed: Original Problem not possible!{bcolors.ENDC}\n")
                raise NoSolution("[phase1] The Original Problem is not possible")
            else:
                # 2) Artificial variable in Base with 0 cost ==>
                #    Simplex Algorithm on columns with cij>=0 and pivot also negative
                while len(phase_tableau.B[check]) > 0:
                    i_art_col = phase_tableau.B[check][0]  # column I want to get out from the Base
                    i_row = np.argmax(phase_tableau.A[:, i_art_col])
                    pivot_done = False
                    for j in range(0, phase_tableau.A.shape[1]):
                        if j not in phase_tableau.B and j not in artificial_base:
                            if phase_tableau.A[i_row, j] != 0:
                                phase_tableau.__pivoting(i_row, j)
                                phase_tableau._base()
                                print(phase_tableau)
                                pivot_done = True
                                break

                    # I can't find a good candidate as pivot ==> all 0 in
                    if not pivot_done:
                        raise RankAWrong(f"[phase1] The Rank of the constraints matrix is not "
                                         f"{self.A.shape[0]}, eliminate the row number {i_row}")
                    check = np.isin(phase_tableau.B, artificial_base)

                self.A = copy.deepcopy(phase_tableau.A[:, :self.A.shape[1]])
                self.B = copy.deepcopy(phase_tableau.B)
                self.b = copy.deepcopy(phase_tableau.b)
                self._z = phase_tableau._z
                self.__azzera_costi_base()
                self.save_sol()
                if self.v:
                    print(f"{bcolors.OKGREEN}||=== === === === ===> Phase 1 Completed!{bcolors.ENDC}(case 2)\n\n")

    def _add_variable(self, new_c, new_a):
        if self.v:
            print("Adding new variables")
        if len(new_a) != self.A.shape[0]:
            raise DimensionError("[_add_variable] new_a's dimension incorrect.")
        if len(new_c) != new_a.shape[1]:
            raise DimensionError("[_add_variable] new_c's dimension incorrect.")

        self.c = np.append(self.c, new_c)
        self.A = np.c_[self.A, new_a]

    def _add_constraint(self, new_r, new_b):
        if self.v:
            print("Adding new constraints")  # constraint = new raw
        if new_r.shape[1] != self.A.shape[1]:
            raise DimensionError("[_add_constraint] new_r's dimension incorrect.")
        if len(new_b) != new_r.shape[0]:
            raise DimensionError("[_add_constraint] new_b's dimension incorrect.")

        self.b = np.append(self.b, new_b)
        self.A = np.vstack((self.A, new_r))

    @property
    def sol(self):  # Tableau always for a min problem
        return -1*self._z

    def save_sol(self):
        var_val = self.var_values()
        self.history.append((var_val, self.sol))

    def var_values(self):
        var_val = np.zeros(len(self.var), dtype=float)
        for i in self.var:
            if i in self.B:
                var_val[i] = np.dot(self.A[:, i], self.b)
        return var_val

    def __str__(self):
        width = 1
        prec = 4
        align = '>'
        s = []
        form = (len(self.c))*' {:{align} {width}.{prec}f} |'
        s.append('\x1b[0;30;41m' + form.format(*self.c, align=align, width=width, prec=prec) +
                 '\x1b[0m' + '\x1b[0;30;42m {:{align} {width}.{prec}f} \x1b[0m'.format(self._z, align=align,
                                                                                       width=width, prec=prec))
        for i, row in enumerate(self.A):
            riga = ""
            for j in range(0, self.A.shape[1]):
                r = ' {:{align} {width}.{prec}f} |' if j not in self.B else \
                    '\x1b[0;30;44m {:{align} {width}.{prec}f} |\x1b[0m'
                riga = riga + r
            s.append(riga.format(*row, align=align, width=width, prec=prec) +
                     '\x1b[0;30;43m {:{align} {width}.{prec}f} \x1b[0m'.format(self.b[i], align=align,
                                                                               width=width, prec=prec))

        s = '\n'.join(s)
        return s
