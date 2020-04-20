
import numpy as np
import math
import copy
import Tableau
from errors import bcolors
sep = '_'


def breadth_first(nodes_list, el):
    nodes_list.append(el)  # add the new el at the end of my nodes_list


def depth_first(nodes_list, el):
    nodes_list.insert(0, el)  # add the new el at the beginning of my nodes_list


class BeB:
    def __init__(self, root: Tableau, insert_rule=breadth_first, v=True):
        self.nodes = list()  # (Tableau, idx, LB)
        self.explored = list()  # TODO for making a nice and beautiful tree print
        self.insert_rule = insert_rule
        self.add(root)
        self.z = math.inf
        self.best_int_sol = None
        self.v = v

        if self.v:
            print("\nRoot Node")
            print(root)
            print(root.var_values())

    def add(self, el, level=None, LB=-1*math.inf):
        if level is None:
            level = '0'
        self.insert_rule(self.nodes, (el, level, LB))

    def isend(self):
        return False if len(self.nodes) > 0 else True

    def expand(self):
        if len(self.nodes) == 0:
            print("No Nodes to explore !!!")
            return False

        el = self.nodes.pop(0)
        n = el[0]
        idx = el[1]
        LB = el[2]

        if self.v:
            print(f"\nExpanding Node: {idx} ...")

        if LB >= self.z:
            if self.v:
                print(f"{bcolors.UNDERLINE}Node Killed !!!{bcolors.ENDC}")
            self.explored.append(n)
            return True

        while not n.isend():
            n.step()

        var_val = n.var_values()  # solution val
        int_var = True
        for j, val in enumerate(var_val):
            int_val = int(val)
            if val - int_val != 0:  # ok decimal variable component
                int_var = False
                temp_t = copy.deepcopy(n)
                # Create 2 node adding two constraints
                # Constraint 1: xj + s = int(var)
                new_cons = np.zeros(temp_t.A.shape[1], dtype=float)
                new_cons[temp_t.var[j]] = 1
                temp_t._add_constraint(np.array([new_cons]), [int_val])

                new_col = np.zeros(temp_t.A.shape[0], dtype=float)
                new_col[-1] = 1
                new_c = np.array([0], dtype=float)
                temp_t._add_variable(new_c, new_col[:, None])

                if not temp_t._base():
                    try:
                        temp_t.phase1()

                        new_lev_idx = idx + sep + str(j * len(n.var))
                        self.add(temp_t, new_lev_idx, math.ceil(n.sol))
                        if self.v:
                            print(f"{bcolors.OKGREEN}Generate and Added Node "
                                  f"{new_lev_idx}{bcolors.ENDC} from variable: {j}")
                    except:
                        if self.v:
                            print(f"{bcolors.WARNING}Discarded Node {new_lev_idx}{bcolors.ENDC} from variable: {j}")
                        pass

                # Constraint 2: xj -s = int(var) + 1 or -xj +s = -int(var) - 1
                temp_t = copy.deepcopy(n)
                new_cons = np.zeros(temp_t.A.shape[1], dtype=float)
                new_cons[temp_t.var[j]] = 1
                temp_t._add_constraint(np.array([new_cons]), [int_val+1])
                new_col = np.zeros(temp_t.A.shape[0], dtype=float)
                new_col[-1] = -1
                temp_t._add_variable(new_c, new_col[:, None])

                if not temp_t._base():
                    try:
                        temp_t.phase1()
                        new_lev_idx = idx + sep + str(j * len(n.var) + 1)
                        self.add(temp_t, new_lev_idx, math.ceil(n.sol))
                        if self.v:
                            print(f"{bcolors.OKGREEN}Generate and Added Node "
                                  f"{new_lev_idx}{bcolors.ENDC} from variable: {j}")
                    except:
                        if self.v:
                            print(f"{bcolors.WARNING}Discarded Node {new_lev_idx}{bcolors.ENDC} from variable: {j}")
                        pass

        if int_var:  # Found integer variables
            if self.v:
                print(f"{bcolors.OKGREEN}{bcolors.UNDERLINE}Integer Solution Found, z updated! ({var_val}){bcolors.ENDC}")
            self.z = n.sol
            self.best_int_sol = var_val

        self.explored.append(n)
        return True

    def __str__(self):
        if len(self.nodes) > 0:
            return ', '.join(map(str, self.nodes))
        else:
            return "No elements"

