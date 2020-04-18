
import numpy as np
from errors import DimensionError, NoBase, bcolors
import copy


class Tableau:
    def __init__(self, c, A, b, rule, B=None):
        self.c = c  # cost vector
        self.A = A  # constraint matrix coefficients
        self.b = b  # constant terms vector
        # self.B = np.zeros(self.A.shape[0], dtype=int)  # TODO if this not exist make the Fase1
        self.B = np.repeat(-1, self.A.shape[0])
        self.rule = rule  # Function to choose wich column enter to the Base
        self._z = float(0)

        # Check dimensions length of c, A, and b
        m = self.A.shape[0]  # num of rows
        n = self.A.shape[1]  # num of columns
        if not len(self.c) == n:
            raise DimensionError("Cost vector length must be equal to n(# A Columns)")
        if not len(self.b) == m:
            raise DimensionError("Constant terms length must be equal to m(# A Rows)")

        print(self)
        if B is not None:
            self.B = np.array(B, dtype=int)
        else:
            # applying phase 1
            if not self._base():
                print(f"{bcolors.WARNING}Impossibile trovare una Base di partenza!{bcolors.ENDC}")
                self.phase1()
                # print(self)
                # self.__azzera_costi_base()

    """
    # Final Tableau if all cost coefficients are positive OR it is not possible to indentify a feasible base
    """
    def isend(self):
        if not self._base():
            print(f"{bcolors.FAIL}Feaseble Base does not exist!{bcolors.ENDC}")
            raise NoBase("Feaseble Base does not exist!")
            return True

        if np.amin(self.c) < 0:
            return False
        else:
            return True

    def step(self, rule=None):
        print("Eseguendo Pivoting...")
        #TODO before pivoting I want to save the states to take track of all the steps

        # for pivoting I need a feasible base
        if not self._base():
            print(f"{bcolors.WARNING}Pivoting not possible, a feasible Base does not exist.{bcolors.ENDC}")
            return False

        if np.sum(self.c[self.B]) != 0:
            self.__azzera_costi_base()

        if self.isend():
            print("Stop Pivoting - End!")
            return True
        if not rule:
            rule = self.rule
        j = rule(self.c)
        pivot = self._pivot(j)
        i = pivot[0]
        p = self.A[i, j]
        print("Individuato Pivot:{:.3f} in colonna: {}, riga: {}".format(p, j, i+1))
        # column j enter to the Base and the corresponding one, consequently, exit
        i = i + 1
        A = np.column_stack((self.A, self.b))
        A = np.row_stack((np.append(self.c, self._z), A))
        # riga del pivot da dividere per il pivot stesso
        A[i] = A[i]/p

        # tutte le altre righe le sommo/sottraggo alla riga del pivot stessa moltiplicata per il valore nella colonna del pivotstesso
        # al fine di annullare qualsiasi termine nella colonna del pivot --> colonna ENTRANTE
        for r in range(0, len(A)):
            if r == i or A[r, j] == 0:
                continue
            A[r] = A[r] - A[r, j] * A[i]

        # qui salvataggio vecchio stato, procedo con l'aggiornamento dello stato
        self.c = A[0, :-1]
        self._z = A[0, -1]
        self.A = A[1:, :-1]
        self.b = A[1:, -1]

        print("...Ending Pivoting")
        #aggiorno la base sapendo che colonna
        self._base()
        return A

    # individuate the coordinate(i,j) of the pivot corresponding on column j
    def _pivot(self, j):
        i = -1
        _min = 1000
        for r in range(0, len(self.A)):
            if self.A[r,j] > 0:
                ba = self.b[r]/self.A[r,j]
                if ba < _min:
                    _min = ba
                    i = r
        return i, j

    """
    # If exist a Base, found it and return True, False otherwise. Check also that the b's values are non negative
    """
    def _base(self):
        if self.__check_positive_b() and \
           (self.A[:, self.B].shape[0] == self.A[:, self.B].shape[1]) and \
           np.allclose(self.A[:, self.B], np.eye(self.A[:, self.B].shape[0])):
            return True
        else:
            print("Individuando una Base...")
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
            print(f"{bcolors.OKGREEN}Base trovata B: {self.B}{bcolors.ENDC}")
            self.__azzera_costi_base()
            return True
        else:
            print(f"{bcolors.WARNING}Base non trovata{bcolors.ENDC}")
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
            print("There's no any Base")
            return False
        for j in self.B:
            if self.c[j] != 0:
                molt = self.c[j]
                self.c = self.c - molt * self.A[np.argmax(self.A[:, j]), :]
                self._z = self._z - molt * self.b[np.argmax(self.A[:, j])]

        print("Base costs set to zero")
        return True

    # Find a Starting Feasible Solution for the Simplex Algorithm
    def phase1(self):
        print(f"\n{bcolors.OKGREEN}||=== === ===> Starting Phase 1...{bcolors.ENDC}")
        phase_tableau = copy.deepcopy(self)
        phase_tableau.c.fill(0)
        m = self.A.shape[0]  # num of rows
        phase_tableau._z = 0
        phase_tableau._add_variable(np.ones(m, dtype=float), np.eye(m))
        phase_tableau.B = np.array(range(len(phase_tableau.c)-m, len(phase_tableau.c)))
        artificial_base = phase_tableau.B
        phase_tableau.__azzera_costi_base()

        print(phase_tableau)
        while not phase_tableau.isend():
            phase_tableau.step()
            print(phase_tableau)

        # 3 Possibilities:
        # 1) All artificial variables out, True variables in Base
        check = np.isin(phase_tableau.B, artificial_base)
        if not check.any():
            self.A = copy.deepcopy(phase_tableau.A[:, :self.A.shape[1]])
            self.B = copy.deepcopy(phase_tableau.B)
            self.b = copy.deepcopy(phase_tableau.b)
            self._z = phase_tableau._z
            print(f"{bcolors.OKGREEN}||=== === ===> Fase 1 Completata!{bcolors.ENDC}\n\n")
            return True
        else:
            print(f"{bcolors.FAIL}||=== === ===> Fase 1 Fallita!{bcolors.ENDC}\n\n")
            return False

    def _add_variable(self, new_c, new_a):
        print("Adding new variables")
        if len(new_a) != self.A.shape[0]:
            raise DimensionError("[__add_variable] new_a's dimension incorrect.")
        if len(new_c) != new_a.shape[1]:
            raise DimensionError("[__add_variable] new_c's dimension incorrect.")

        self.c = np.append(self.c, new_c)
        self.A = np.c_[self.A, new_a]

    def __str__(self):
        width = 1
        prec = 4
        align = '>'
        s = []
        form = (len(self.c))*' {:{align} {width}.{prec}f} |'
        s.append('\x1b[0;30;41m' + form.format(*self.c, align=align, width=width, prec=prec) + '\x1b[0m' + '\x1b[0;30;42m {:{align} {width}.{prec}f} \x1b[0m'.format(self._z, align=align, width=width, prec=prec))
        for i, row in enumerate(self.A):
            riga = ""
            for j in range(0, self.A.shape[1]):
                r = ' {:{align} {width}.{prec}f} |' if j not in self.B else '\x1b[0;30;44m {:{align} {width}.{prec}f} |\x1b[0m'
                riga = riga + r
            s.append(riga.format(*row, align=align, width=width, prec=prec) + '\x1b[0;30;43m {:{align} {width}.{prec}f} \x1b[0m'.format(self.b[i], align=align, width=width, prec=prec))

        s = '\n'.join(s)
        return s


    """
    s = []
        form = (len(self.c))*' {:^{width} 4f} |'
        s.append('\x1b[0;30;41m' + form.format(*self.c, width=5) + '\x1b[0m' + '\x1b[0;30;42m {:^{width} 4f} \x1b[0m'.format(self._z, width=5))
        for i, row in enumerate(self.A):
            riga = ""
            for j in range(0, self.A.shape[1]):
                r = ' {:^{width} 4f} |' if j not in self.B else '\x1b[0;30;44m {:^{width} 4f} |\x1b[0m'
                riga = riga + r
            s.append(riga.format(*row, width=5) + '\x1b[0;30;43m {:^{width} 4f} \x1b[0m'.format(self.b[i], width=5))

        s = '\n'.join(s)
        return s
    """