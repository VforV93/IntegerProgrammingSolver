
import numpy as np


def dantzig_rule(c):
    if np.min(c) < 0:
        return np.argmin(c)
    raise Exception("[dantzig_rule] no valid column")


def bland_rule(c):
    for i, c_el in enumerate(c):
        if c_el < 0:
            return i
    raise Exception("[bland_rule] no valid column")