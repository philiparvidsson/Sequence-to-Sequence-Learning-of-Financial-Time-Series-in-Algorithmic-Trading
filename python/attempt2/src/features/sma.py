#---------------------------------------
# IMPORTS
#---------------------------------------

import numpy as np

#---------------------------------------
# CLASSES
#---------------------------------------

class SMA(object):
    def __init__(self, feature, width=10, hidden=False):
        self.hidden = hidden
        self.dim = feature.dim
        self.feature = feature
        self.width = width
        self.name = "SMA" + str(width) + "_" + feature.name

    def set_idx(self, idx):
        self.idx = idx
        self.feature.set_idx(idx)

    def get_first_y(self, p, ds, i):
        return self.feature.get_first_y(p, ds, i)

    def calc(self, ds, i):
        n = 0
        avg = [0.0 for x in xrange(self.feature.dim)]

        for j in xrange(self.width):
            idx = i - j
            if idx < 0:
                break

            vals = self.feature.calc(ds, idx)

            for k in xrange(self.feature.dim):
                avg[k] += vals[k]

            n += 1

        for k in xrange(self.feature.dim):
            avg[k] /= n

        return avg

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        if self.hidden: return
        self.feature.plot(p, ds, a, b, color, is_pred)
